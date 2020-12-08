import logging
import ssl
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from config import settings


logger = logging.getLogger(__name__)


def send_email_notification(data, subject, contents):
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = settings.EMAIL_FROM_ADDRESS
    message["To"] = data["Email"]

    # Create the plain-text and HTML version of your message
    text = contents

    html = """\
                <html>
                  <body>
                    <p>Salutare {first_name},<br/>
                       <br/>
                       {contents}<br/>
                       <br/>
                       Regards,
                       <br/>
                       <br/>
                       <b>London Romanian SDA Church</b>
                    </p>
                  </body>
                </html>
                """.format(first_name=data['Prenume'], contents=contents)

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)

    try:
        # Create secure connection with server and send email
        context = ssl.create_default_context()
        with smtplib.SMTP(settings.EMAIL_SMTP_HOST, settings.EMAIL_SMTP_PORT) as server:
            server.starttls(context=context)
            server.login(settings.EMAIL_USER_NAME, settings.EMAIL_PASSWORD)
            server.sendmail(settings.EMAIL_FROM_ADDRESS, data["Email"], message.as_string())
            return True

    except smtplib.SMTPException:
        pass

    return False
