from typing import Any, Generic, TypeVar
from uuid import UUID

from fastapi import HTTPException
from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlmodel import paginate
from pydantic import BaseModel
from sqlalchemy import exc
from sqlmodel import Session, SQLModel, func, select
from sqlmodel.sql.expression import Select
from unigate.core.database import get_session

ModelType = TypeVar("ModelType", bound=SQLModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
SchemaType = TypeVar("SchemaType", bound=BaseModel)
T = TypeVar("T", bound=SQLModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: type[ModelType]) -> None:
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        **Parameters**
        * `model`: A SQLModel model class
        * `db_session`: A SQLAlchemy Session instance
        """
        self.model = model
        self.db_session = next(get_session())

    def get_db(self) -> Session:
        return next(get_session())

    def get(self, *, id: UUID | str) -> ModelType | None:
        query = select(self.model).where(self.model.id == id)
        response = self.db_session.exec(query)
        return response.one_or_none()

    def get_by_ids(self, *, list_ids: list[UUID | str]) -> list[ModelType]:
        response = self.db_session.exec(
            select(self.model).where(self.model.id.in_(list_ids))
        )
        return response.scalars().all()

    def get_count(self) -> int:
        response = self.db_session.exec(
            select(func.count()).select_from(select(self.model).subquery())
        )
        return response.one()

    def get_multi(
        self,
        *,
        skip: int = 0,
        limit: int = 100,
        query: T | Select[T] | None = None,
    ) -> list[ModelType]:
        if query is None:
            query = select(self.model).offset(skip).limit(limit).order_by(self.model.id)
        response = self.db_session.exec(query)
        return response.all()

    def get_multi_paginated(
        self,
        *,
        params: Params | None = Params(),
        query: T | Select[T] | None = None,
    ) -> Page[ModelType]:
        if query is None:
            query = select(self.model)
        return paginate(self.db_session, query, params)

    def get_multi_paginated_ordered(
        self,
        *,
        params: Params | None = Params(),
        order_by: str | None = None,
        order: str = "asc",
        query: T | Select[T] | None = None,
    ) -> Page[ModelType]:
        columns = self.model.__table__.columns
        order_by_column = columns.get(order_by, columns["id"])

        if query is None:
            query = select(self.model).order_by(
                order_by_column.asc() if order == "asc" else order_by_column.desc()
            )

        return paginate(self.db_session, query, params)

    def get_multi_ordered(
        self,
        *,
        skip: int = 0,
        limit: int = 100,
        order_by: str | None = None,
        order: str = "asc",
    ) -> list[ModelType]:
        columns = self.model.__table__.columns
        order_by_column = columns.get(order_by, columns["id"])

        query = (
            select(self.model)
            .offset(skip)
            .limit(limit)
            .order_by(
                order_by_column.asc() if order == "asc" else order_by_column.desc()
            )
        )

        response = self.db_session.exec(query)
        return response.scalars().all()

    def create(
        self,
        *,
        obj_in: CreateSchemaType | ModelType,
        created_by_id: UUID | str | None = None,
    ) -> ModelType:
        db_obj = self.model.model_validate(obj_in)  # type: ignore

        if created_by_id:
            db_obj.created_by_id = created_by_id

        try:
            self.db_session.add(db_obj)
            self.db_session.commit()
        except exc.IntegrityError:
            self.db_session.rollback()
            raise HTTPException(
                status_code=409,
                detail="Resource already exists",
            )
        self.db_session.refresh(db_obj)
        return db_obj

    def update(
        self,
        *,
        obj_current: ModelType,
        obj_new: UpdateSchemaType | dict[str, Any] | ModelType,
    ) -> ModelType:
        update_data = (
            obj_new if isinstance(obj_new, dict) else obj_new.dict(exclude_unset=True)
        )
        for field in update_data:
            setattr(obj_current, field, update_data[field])

        self.db_session.add(obj_current)
        self.db_session.commit()
        self.db_session.refresh(obj_current)
        return obj_current

    def remove(self, *, id: UUID | str) -> ModelType:
        response = self.db_session.exec(select(self.model).where(self.model.id == id))
        obj = response.scalar_one()
        self.db_session.delete(obj)
        self.db_session.commit()
        return obj
