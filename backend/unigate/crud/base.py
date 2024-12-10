from typing import Any, Generic, TypeVar
from uuid import UUID

from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import exc
from sqlmodel import Session, SQLModel, func, select
from sqlmodel.sql.expression import SelectOfScalar

from unigate.core.database import get_session

ModelType = TypeVar("ModelType", bound=SQLModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
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

    def get_db_session(self) -> Session:
        return next(get_session())

    def get(
        self, *, id: UUID | str, db_session: Session | None = None
    ) -> ModelType | None:
        db_session = db_session or self.db_session
        query = select(self.model).where(self.model.id == id)  # type: ignore
        response = db_session.exec(query)
        return response.one_or_none()

    def get_by_ids(
        self, *, list_ids: list[UUID | str], db_session: Session | None = None
    ) -> list[ModelType]:
        db_session = db_session or self.db_session
        response = db_session.exec(
            select(self.model).where(self.model.id.in_(list_ids))  # type: ignore
        )
        return response.all()  # type: ignore

    def get_count(self, db_session: Session | None = None) -> int:
        db_session = db_session or self.db_session
        response = db_session.exec(
            select(func.count()).select_from(select(self.model).subquery())
        )
        return response.one()

    def get_multi(
        self,
        *,
        skip: int = 0,
        limit: int = 100,
        query: SelectOfScalar[T] | None = None,
        db_session: Session | None = None,
    ) -> list[ModelType]:
        db_session = db_session or self.db_session
        statement = (
            select(self.model).offset(skip).limit(limit) if query is None else query
        )
        response = db_session.exec(statement)
        return response.all()  # type: ignore

    def get_multi_ordered(
        self,
        *,
        skip: int = 0,
        limit: int = 100,
        order_by: str | None = None,
        order: str = "asc",
        db_session: Session | None = None,
    ) -> list[ModelType]:
        db_session = db_session or self.db_session
        columns = self.model.__table__.columns  # type: ignore
        order_by_column = columns.get(order_by, columns["id"])  # type: ignore

        query = (
            select(self.model)
            .offset(skip)
            .limit(limit)
            .order_by(
                order_by_column.asc() if order == "asc" else order_by_column.desc()  # type: ignore
            )
        )

        response = db_session.exec(query)
        return response.all()  # type: ignore

    def create(
        self,
        *,
        obj_in: CreateSchemaType | ModelType,
        update: dict[str, Any] | None = None,
        db_session: Session | None = None,
    ) -> ModelType:
        db_session = db_session or self.db_session
        db_obj = self.model.model_validate(obj_in, update=update)

        try:
            db_session.add(db_obj)
            db_session.commit()
        except exc.IntegrityError:
            self.db_session.rollback()
            raise HTTPException(
                status_code=409,
                detail="Resource already exists",
            )
        db_session.refresh(db_obj)
        return db_obj

    def update(
        self,
        *,
        obj_current: ModelType,
        obj_new: UpdateSchemaType | dict[str, Any] | ModelType,
        db_session: Session | None = None,
    ) -> ModelType:
        db_session = db_session or self.db_session
        update_data = (
            obj_new
            if isinstance(obj_new, dict)
            else obj_new.model_dump(exclude_unset=True)
        )
        for field in update_data:
            setattr(obj_current, field, update_data[field])

        db_session.add(obj_current)
        db_session.commit()
        db_session.refresh(obj_current)
        return obj_current

    def remove(self, *, id: UUID | str, db_session: Session | None) -> ModelType:
        db_session = db_session or self.db_session
        response = db_session.exec(select(self.model).where(self.model.id == id))  # type: ignore
        obj = response.one()
        self.db_session.delete(obj)
        self.db_session.commit()
        return obj
