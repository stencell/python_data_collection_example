from email.mime.text import MIMEText
import smtplib
import os

def send_email(email, height, average_height, height_count):
    #from_email = "changeme"
    #from_password = "changeme"
    from_email = os.environ['EMAIL_ADDRESS']
    from_password = os.environ['EMAIL_PASS']
    to_email = email
    subject = "Height Data Analysis"
    message = "Your height is <strong>%s</strong>. Average height of %s people is %s" % (height, height_count, average_height)
    msg=MIMEText(message, "html")
    msg['Subject'] = subject
    msg['To'] = to_email
    msg['From'] = from_email
    gmail=smtplib.SMTP('smtp.gmail.com', 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(from_email, from_password)
    gmail.send_message(msg)