import sendgrid
from sendgrid.helpers.mail import *

from unigate.core.config import settings


class Mailer:
    _from = "i@abida.me"

    def __init__(self, to, subject, content, cc=None, bcc=None):
        self.to = to
        self.subject = subject
        self.content = content
        self.cc = cc
        self.bcc = bcc

    def send(self):
        sg = sendgrid.SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)

        sandbox_mode = SandBoxMode(False)
        mail_settings = MailSettings()
        mail_settings.sandbox_mode = sandbox_mode

        from_email = Email(self._from)
        to_email = To(self.to)
        subject = self.subject
        content = Content("text/plain", self.content)
        mail = Mail(from_email, to_email, subject, content)
        mail.mail_settings = mail_settings
        response = sg.client.mail.send.post(request_body=mail.get())
        print(response.status_code)
        print(response.body)
        print(response.headers)
