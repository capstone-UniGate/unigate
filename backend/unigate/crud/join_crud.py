import datetime
import uuid

import pytz
from loguru import logger
from sqlalchemy import exc
from sqlmodel import select
from unigate.models import Group, Join, Request
from unigate.utils.mail import Mailer

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

        self.create(
            obj_in=Join(
                date=datetime.datetime.now(tz=pytz.timezone("Europe/Rome")).date(),
                student_id=student_id,
                group_id=group_id,
            )
        )
        return "Insert successful"

    def check_double_enrollment(
        self, student_id: uuid.UUID, category: str | None = None
    ) -> bool:
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

    def join_private_group(self, student_id: uuid.UUID, group_id: uuid.UUID) -> str:
        group = self.group_crud.get(id=group_id)
        student = self.student_crud.get(id=student_id)

        if group is None or student is None:
            return "Either the group or the student doesn't exist"

        if not self.check_double_enrollment(student_id, group.category):
            return "You are already enrolled in a team for the same course"

        self.request_crud.create_request(
            Request(
                student_id=student_id,
                group_id=group_id,
            )
        )

        # Fetch the super student (group admin) for the group
        super_student = self.super_student_crud.get_by_group_id(group_id)
        if super_student:
            admin_student = self.student_crud.get(id=super_student.student_id)
            if (
                admin_student and admin_student.email
            ):  # Ensure the admin has an email address
                self.send_join_request_email(
                    admin_email=admin_student.email,  # This ensures the super student's email is used
                    student_name=student.name,
                    group_name=group.name,
                )

        return "Join request submitted successfully"

    def send_join_request_email(
        admin_email: str, student_name: str, group_name: str
    ) -> None:
        to = admin_email
        subject = f"Join Request for {group_name}"
        content = (
            f"Hello,\n\n"
            f"You have a new join request for the group '{group_name}'.\n"
            f"Student: {student_name}\n\n"
            f"Please review and take the necessary action.\n\n"
            f"Best regards,\n Unigate"
        )

        mail = Mailer(to, subject, content)
        mail.send()
        logger.info("Email sent successfully to the admin.")


join_crud = CRUDJoin(Join)
