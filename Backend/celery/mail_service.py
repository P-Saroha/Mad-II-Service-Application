import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SMTP_SERVER = "localhost"
SMTP_PORT = 1025
SENDER_EMAIL = 'Parveen@gmail.com'
SENDER_PASSWORD = ''  # Not used here but typically needed for real SMTP services

def send_email(to, subject, content):
    msg = MIMEMultipart()
    msg['To'] = to
    msg['Subject'] = subject
    msg['From'] = SENDER_EMAIL

    msg.attach(MIMEText(content, 'html'))

    with smtplib.SMTP(host=SMTP_SERVER, port=SMTP_PORT) as client:
        client.send_message(msg)

# Run only for local testing
if __name__ == "__main__":
    send_email('parveen@example', 'Test Email', '<h1> Welcome to Household Services Application </h1>')
