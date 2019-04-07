"""
Email Service class to send the created markdown report to the given emails.

Parameters:
"""
import os
import markdown2
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


class EmailService:
    """
    Creates the email client.

    Use this object to send emails to the given receivers.

    Parameters:
        from_email <str> The email address of the sender
        to_emails <str> or <tuple> The email address(es) of the recipient(s)
        subject <str> Subject of the email
        plain_content <str> Plain text body of the email
        html_content <str> HTML formatted body of the email
    """
    def __init__(
        self,
        from_email=None,
        to_emails=None,
        cc_emails=None,
        subject=None,
        md_report=None,
    ):
        self._client = SendGridAPIClient(os.environ.get('SENDGRID_KEY'))
        self._message = Mail(
            from_email=from_email,
            to_emails=to_emails,
            subject=subject,
            html_content=markdown2.markdown(md_report),
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
