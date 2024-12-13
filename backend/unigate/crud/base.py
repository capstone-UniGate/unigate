from typing import Any, Generic, TypeVar
from uuid import UUID

from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import exc
from sqlmodel import Session, SQLModel, func, select
from sqlmodel.sql.expression import SelectOfScalar

ModelType = TypeVar("ModelType", bound=SQLModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
T = TypeVar("T", bound=SQLModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: type[ModelType]) -> None:
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        **Parameters**
        """
        self.model = model

    def get(self, *, id: UUID | str, session: Session) -> ModelType | None:
        query = select(self.model).where(self.model.id == id)  # type: ignore
        response = session.exec(query)
        return response.one_or_none()

    def get_by_ids(
        self, *, list_ids: list[UUID | str], session: Session
    ) -> list[ModelType]:
        response = session.exec(
            select(self.model).where(self.model.id.in_(list_ids))  # type: ignore
        )
        return response.all()  # type: ignore

    def get_count(self, session: Session) -> int:
        response = session.exec(
            select(func.count()).select_from(select(self.model).subquery())
        )
        return response.one()

    def get_multi(
        self,
        *,
        skip: int = 0,
        limit: int = 100,
        query: SelectOfScalar[T] | None = None,
        session: Session,
    ) -> list[ModelType]:
        statement = (
            select(self.model).offset(skip).limit(limit) if query is None else query
        )
        response = session.exec(statement)
        return response.all()  # type: ignore

    def get_multi_ordered(
        self,
        *,
        skip: int = 0,
        limit: int = 100,
        order_by: str | None = None,
        order: str = "asc",
        session: Session,
    ) -> list[ModelType]:
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

        response = session.exec(query)
        return response.all()  # type: ignore

    def get_all(self, *, session: Session) -> list[ModelType]:
        response = session.exec(select(self.model))
        return response.all()  # type: ignore

    def create(
        self,
        *,
        obj_in: CreateSchemaType | ModelType,
        update: dict[str, Any] | None = None,
        session: Session,
    ) -> ModelType:
        db_obj = self.model.model_validate(obj_in, update=update)

        try:
            session.add(db_obj)
            session.commit()
        except exc.IntegrityError:
            session.rollback()
            raise HTTPException(
                status_code=409,
                detail="Resource already exists",
            )
        session.refresh(db_obj)
        return db_obj

    def update(
        self,
        *,
        obj_current: ModelType,
        obj_new: UpdateSchemaType | dict[str, Any] | ModelType,
        session: Session,
    ) -> ModelType:
        update_data = (
            obj_new
            if isinstance(obj_new, dict)
            else obj_new.model_dump(exclude_unset=True)
        )
        for field in update_data:
            setattr(obj_current, field, update_data[field])

        session.add(obj_current)
        session.commit()
        session.refresh(obj_current)
        return obj_current

    def remove(self, *, id: UUID | str, session: Session) -> ModelType:
        response = session.exec(select(self.model).where(self.model.id == id))  # type: ignore
        obj = response.one()
        session.delete(obj)
        session.commit()
        return obj
