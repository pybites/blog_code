from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

PYBITES_EMAIL = 'pybitesblog@gmail.com'

def email(subject, content, recipients=None):
    if not recipients:
        recipients = [PYBITES_EMAIL]
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = PYBITES_EMAIL
    msg['To'] = ", ".join(recipients)
    part = MIMEText(content, 'html')
    msg.attach(part)
    s = smtplib.SMTP('localhost')
    s.sendmail(PYBITES_EMAIL, recipients, msg.as_string())
    s.quit()

if __name__ == "__main__":
    email(["info@bobbelderbos.com"], "test mail", "hello bob")
