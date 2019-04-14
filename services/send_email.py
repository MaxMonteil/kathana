"""
Email Service class to send the created markdown report to the given emails.
"""

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os


class EmailService:
    """
    Creates the email client.

    Use this object to send emails to the given receivers.

    Parameters:
        from_email <str> The email address of the sender
        to_emails <str> or <tuple> The email address(es) of the recipient(s)
        cc_emails <list> collection of emails addresss to CC with the email
        subject <str> Subject of the email
        report <str> HTML formatted body of the email
    """
    def __init__(
        self,
        from_email=None,
        to_emails=None,
        cc_emails=None,
        subject=None,
        report=None,
    ):
        self._client = SendGridAPIClient(os.environ.get('SENDGRID_KEY'))
        self._message = Mail(
            from_email=from_email,
            to_emails=to_emails,
            subject=subject,
            html_content=report,
        )

        if cc_emails is not None:
            self._message.cc = cc_emails

    def send_email(self):
        try:
            response = self._client.send(self._message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print(e)
