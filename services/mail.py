import smtplib
import ssl
import logging

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from config import MailConfig

port = 465  # For SSL


class MailService:

    def __init__(self, conf: MailConfig):
        self.subject = conf.default_subject
        self.body = conf.default_body
        self.sender_email = conf.sender_email
        self.password = conf.password
        self.default_receiver = conf.default_receiver
        self.default_attachment_name = conf.default_attachment_name
        self.context = ssl.create_default_context()

    # Create a multipart message and set headers

    def send_mail(self, attachment: str, recipient=None):
        if recipient is None:
            recipient = self.default_receiver
        message = MIMEMultipart()
        message["From"] = self.sender_email
        message["To"] = recipient
        message["Subject"] = self.subject

        # Add body to email
        message.attach(MIMEText(self.body, "plain"))
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment)
        encoders.encode_base64(part)

        # Add header as key/value pair to attachment part
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {self.default_attachment_name}",
        )
        # Add attachment to message and convert message to string
        message.attach(part)
        text = message.as_string()

        # Log in to server using secure context and send email
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=self.context) as server:
            server.login(self.sender_email, self.password)
            server.sendmail(self.sender_email, recipient, text)
            logging.info(f"mail sent to {recipient}")
