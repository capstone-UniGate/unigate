import datetime
import uuid

from loguru import logger
from sqlmodel import Field, SQLModel  # type: ignore

from unigate.utils.mail import Mailer


class Join(SQLModel, table=True):
    __tablename__ = "joins"  # type: ignore

    date: datetime.date | None = Field(default_factory=datetime.date.today)

    student_id: uuid.UUID = Field(
        foreign_key="students.id", primary_key=True, ondelete="CASCADE"
    )
    group_id: uuid.UUID = Field(
        foreign_key="groups.id", primary_key=True, ondelete="CASCADE"
    )

    @staticmethod
    def send_join_request_email(
        admin_email: str, student_name: str, group_name: str
    ) -> None:
        """
        Sends an email to the group admin notifying them about a join request.

        :param admin_email: Email address of the group admin
        :param student_name: Name of the student requesting to join
        :param group_name: Name of the private group
        """
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
