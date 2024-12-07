import uuid

from sqlmodel import select
from unigate.models import Blocked, Group

from .base_crud import CRUDBase
from .group_crud import group_crud
from .student_crud import student_crud


class CRUDBlocked(CRUDBase[Blocked, Blocked, Blocked]):
    def block_student(self, student_id: uuid.UUID, group_id: uuid.UUID) -> str:
        # Check if the student and group exist
        if group_crud.get(id=group_id) is None:
            return "The group doesn't exist"
        if student_crud.get(id=student_id) is None:
            return "The student doesn't exist"

        # Check if already blocked
        if self.is_student_blocked(student_id, group_id):
            return "The student is already blocked in this group"

        # Block the student
        self.create(
            obj_in=Blocked(
                student_id=student_id,
                group_id=group_id,
            )
        )
        return "Student successfully blocked"

    def unblock_student(self, student_id: uuid.UUID, group_id: uuid.UUID) -> str:
        # Find the block entry
        db_session = self.get_db()
        response = db_session.exec(
            select(self.model)
            .where(self.model.student_id == student_id)
            .where(self.model.group_id == group_id)
        )
        block_entry = response.one_or_none()

        if block_entry is None:
            return "The student is not blocked in this group"

        # Delete the block entry
        self.delete(block_entry)
        return "Student successfully unblocked"

    def is_student_blocked(self, student_id: uuid.UUID, group_id: uuid.UUID) -> bool:
        # Check if the student is blocked in the given group
        db_session = self.get_db()
        statement = (
            select(self.model)
            .where(self.model.student_id == student_id)
            .where(self.model.group_id == group_id)
        )
        result = db_session.exec(statement)
        return result.one_or_none() is not None

    def get_blocked_groups(self, student_id: uuid.UUID) -> list[Group]:
        # Get all groups where the student is blocked
        statement = select(Group).join(Blocked).where(Blocked.student_id == student_id)
        return self.get_multi(query=statement)

    def get_blocked_students(self, group_id: uuid.UUID) -> list[uuid.UUID]:
        # Get all students blocked in the group
        db_session = self.get_db()
        statement = select(self.model.student_id).where(self.model.group_id == group_id)
        result = db_session.exec(statement)
        return result.all()


blocked_crud = CRUDBlocked(Blocked)
