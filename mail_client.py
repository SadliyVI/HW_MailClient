import email
import smtplib
import imaplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class MailClient:
    """
    A class to handle e-mail operations such as sending and receiving e-mails.

    Attributes:
        login (str): The email address used for authentication.
        password (str): The password for the email account.
        smtp_server (str): The SMTP server address.
        imap_server (str): The IMAP server address.
        smtp_port (int): The port number for the SMTP server.
    """

    def __init__(self, login: str, password: str,
                 smtp_server: str = 'smtp.gmail.com',
                 imap_server: str = 'imap.gmail.com',
                 smtp_port: int = 587):
        """
        Initialize the MailClient with the given parameters.

        Args:
            login (str): The email address used for authentication.
            password (str): The password for the email account.
            smtp_server (str, optional): The SMTP server address.
                                         Defaults to 'smtp.gmail.com'.
            imap_server (str, optional): The IMAP server address.
                                         Defaults to 'imap.gmail.com'.
            smtp_port (int, optional): The port number for the SMTP server.
                                       Defaults to 587.
        """
        self.login = login
        self.password = password
        self.smtp_server = smtp_server
        self.imap_server = imap_server
        self.smtp_port = smtp_port

    def send_email(self, subject: str, recipients: list, message: str) -> None:
        """
        Send an e-mail to the specified recipients.

        Args:
            subject (str): The subject of the email.
            recipients (list): A list of email addresses to send the email to.
            message (str): The body of the email.

        Returns:
            None
        """
        msg = MIMEMultipart()
        msg['From'] = self.login
        msg['To'] = ', '.join(recipients)
        msg['Subject'] = subject
        msg.attach(MIMEText(message))

        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.starttls()
            server.login(self.login, self.password)
            server.sendmail(self.login, recipients, msg.as_string())

    def receive_email(self, header: str = None) -> email.message.Message:
        """
        Retrieve the latest email with the specified header from the inbox.

        Args:
            header (str, optional): The subject header to search for.
                                    If None, retrieves the latest email.
                                    Defaults to None.
        Returns:
            e-mail.message.Message: The latest e-mail message matching the
            header criteria.
        Raises:
            ValueError: If no emails are found with the specified header.
        """
        with imaplib.IMAP4_SSL(self.imap_server) as mail:
            mail.login(self.login, self.password)
            mail.select('inbox')

            criterion = f'(HEADER Subject "{header}")' if header else 'ALL'
            _, data = mail.uid('search', None, criterion)

            if not data[0]:
                raise ValueError('Нет писем с указанным заголовком')

            latest_email_uid = data[0].split()[-1]
            _, data = mail.uid('fetch', latest_email_uid, '(RFC822)')

        return email.message_from_bytes(data[0][1])