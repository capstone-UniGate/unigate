import sendgrid  # type: ignore
from loguru import logger
from sendgrid.helpers.mail import (  # type: ignore
    Content,
    Email,
    Mail,
    MailSettings,
    SandBoxMode,
    To,
)

from unigate.core.config import settings


class Mailer:
    _from = "i@abida.me"

    def __init__(self, to: str | list[str], subject: str, content: str) -> None:
        self.to = to
        self.subject = subject
        self.content = content

    def send(self) -> None:
        sg = sendgrid.SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)

        sandbox_mode = SandBoxMode(enable=False)
        mail_settings = MailSettings()
        mail_settings.sandbox_mode = sandbox_mode

        from_email = Email(self._from)
        to_email = To(self.to)
        subject = self.subject
        content = Content("text/plain", self.content)
        mail = Mail(from_email, to_email, subject, content)
        mail.mail_settings = mail_settings
        response = sg.client.mail.send.post(request_body=mail.get())  # type: ignore
        logger.debug(response.status_code)  # type: ignore
        logger.debug(response.body)  # type: ignore
        logger.debug(response.headers)  # type: ignore
