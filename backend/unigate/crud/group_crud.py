from sqlmodel import select

from unigate.models import Group

from .base_crud import CRUDBase


class CRUDGroup(CRUDBase[Group, Group, Group]):
    def get_by_name(self, *, name: str) -> Group | None:
        db_session = self.get_db()
        statement = select(self.model).where(self.model.name == name)
        result = db_session.exec(statement)
        return result.scalar_one_or_none()


group_crud = CRUDGroup(Group)
