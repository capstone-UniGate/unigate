import datetime

from fastapi import Depends
from sqlmodel import Session, and_, select

from unigate.core.database import get_session
from unigate.crud.base import CRUDBase
from unigate.enums import RequestStatus
from unigate.models import Group
from unigate.models.request import Request
from unigate.models.student import Student
from unigate.schemas.group import GroupCreate


class CRUDGroup(CRUDBase[Group, GroupCreate, Group]):
    def get_by_name(
        self, *, name: str, db_session: Session = Depends(get_session)
    ) -> Group | None:
        statement = select(self.model).where(self.model.name == name)
        result = db_session.exec(statement)
        return result.one_or_none()

    def join(self, *, group: Group, student: Student, session: Session) -> Group:
        group.students.append(student)
        session.add(group)
        session.commit()
        session.refresh(group)
        return group

    def leave(self, *, group: Group, student: Student, session: Session) -> Group:
        group.students.remove(student)
        session.add(group)
        session.commit()
        session.refresh(group)
        return group

    def create_request(
        self, *, group: Group, student: Student, session: Session
    ) -> Group:
        request = Request(
            student_id=student.id,
            group_id=group.id,
            student=student,
            group=group,
            status=RequestStatus.PENDING,
        )
        group.requests.append(request)
        session.add(group)
        session.commit()
        session.refresh(group)
        session.refresh(request)
        return group

    def approve_request(self, *, request: Request, session: Session) -> Request:
        request.status = RequestStatus.APPROVED
        request.group.students.append(request.student)
        session.add(request)
        session.commit()
        session.refresh(request)
        return request

    def reject_request(self, *, request: Request, session: Session) -> Request:
        request.status = RequestStatus.REJECTED
        session.add(request)
        session.commit()
        session.refresh(request)
        return request

    def block_request(self, *, request: Request, session: Session) -> Request:
        request.status = RequestStatus.BLOCKED
        request.group.blocked_students.append(request.student)
        session.add(request)
        session.commit()
        session.refresh(request)
        return request

    def block_user(self, *, group: Group, student: Student, session: Session) -> Group:
        if student in group.students:
            group.students.remove(student)
        group.blocked_students.append(student)
        session.add(group)
        session.commit()
        session.refresh(group)
        return group

    def unblock_user(
        self, *, group: Group, student: Student, session: Session
    ) -> Group:
        group.blocked_students.remove(student)
        session.add(group)
        session.commit()
        session.refresh(group)
        return group

    def delete_request(
        self, *, group: Group, session: Session, request: Request
    ) -> None:
        group.requests.remove(request)  # type: ignore
        session.delete(request)
        session.commit()
        session.refresh(group)

    def get_groups_course(self, *, course_name: str, session: Session) -> list[Group]:
        statement = select(self.model).where(self.model.course_name == course_name)
        result = session.exec(statement)
        return result.all()  # type: ignore

    def get_groups_exam(
        self, *, course_name: str, session: Session, date: str
    ) -> list[Group]:
        parsed_date = datetime.datetime.strptime(date, "%Y-%m-%d").date()  # noqa: DTZ007
        statement = select(self.model).where(
            and_(
                self.model.course_name == course_name,
                self.model.exam_date == parsed_date,
            )
        )
        result = session.exec(statement)
        return result.all()  # type: ignore


group = CRUDGroup(Group)
