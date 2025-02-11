import datetime

from fastapi import Depends
from sqlmodel import Session, and_, select

from unigate.core.database import get_session
from unigate.crud.base import CRUDBase
from unigate.enums import GroupType, RequestStatus
from unigate.models import Group
from unigate.models.request import Request
from unigate.models.student import Student
from unigate.schemas.group import (
    GroupCreate,
    NumberMembersOfGroups,
    NumberOfGroupsResponse,
)


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

    def search(
        self,
        session: Session,
        course: str,
        is_public: bool = None,
        exam_date: str = None,
        participants: int = None,
        order: str = None,
    ) -> list[Group]:
        query = select(Group)

        if course:
            query = query.where(Group.course_name == course)

        if is_public is not None:
            if is_public:
                query = query.where(Group.type == GroupType.PUBLIC)
            else:
                query = query.where(Group.type == GroupType.PRIVATE)

        if exam_date:
            query = query.where(Group.exam_date == exam_date)

        if order == "Newest":
            query = query.order_by(Group.date.desc())
        elif order == "Oldest":
            query = query.order_by(Group.date)

        groups = self.get_multi(session=session, query=query)

        if participants:
            return [group for group in groups if len(group.students) >= participants]

        return groups

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

    def number_of_groups(
        self, *, course_name: str, session: Session
    ) -> NumberOfGroupsResponse:
        groups = self.get_groups_course(course_name=course_name, session=session)
        count = len(groups)
        group_names = [str(group.name) for group in groups]
        return {"count": count, "groups": group_names}

    def average_members(
        self, *, course_name: str, session: Session
    ) -> NumberMembersOfGroups:
        groups = self.get_groups_course(course_name=course_name, session=session)
        members = [len(group.students) for group in groups]
        return {
            "avg": sum(members) / len(members),
            "min": min(members),
            "max": max(members),
            "members": {str(group.name): len(group.students) for group in groups},
        }


group = CRUDGroup(Group)
