import datetime
import uuid

from sqlalchemy import exc
from sqlmodel import select
from unigate.models import Group, Join

from .base_crud import CRUDBase
from .group_crud import group_crud
from .student_crud import student_crud


class CRUDJoin(CRUDBase[Join, Join, Join]):
    def join_public_group(self, student_id: uuid.UUID, group_id: uuid.UUID) -> str:
        group = group_crud.get(id=group_id)
        if group is None or student_crud.get(id=student_id) is None:
            return "Either the group or the student don't exist"
        if not self.check_double_enrollment(student_id, group.category):
            return "You are already enrolled in a team for the same course"

        self.create(obj_in=Join(date=datetime.date.today(), student_id=student_id, group_id=group_id))
        return "Insert successful"

    def check_double_enrollment(self, student_id: uuid.UUID, category: str | None = None) -> bool:
        db_session = self.get_db()
        try:
            statement = (
                select(Group)
                .join(Join)
                .where(Join.student_id == student_id)
                .where(Group.category == category)
            )
            result = db_session.exec(statement)
            return result.one_or_none() is None
        except exc.MultipleResultsFound:
            return False

join_crud = CRUDJoin(Join)
