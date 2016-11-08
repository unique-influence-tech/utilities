"""
Utilities commonly used to transfer data.
"""
import os

from smtplib import SMTP
from data import auth
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

def send_email(package, message=None, file_path=None, send=True):
    """A function that makes sending emails with attachments 
    repeatable and easier.
    
    :params package: dict, containing fields
    :params message: str, optional message to include in email
    :params file_path: str, absolute filepath
    :params send: bool, safety mechanism
    
    package is a dict object with the following fields:
        from :: str, superficial sender
        to :: str, superficial recipient
        subject :: email subject
        sender :: str, email of sender
        recipients :: str or list, the emails of the recipients
    """
    keys = set(package.keys()) 
    check = set(['from','to','subject','sender','recipients'])

    if keys != check:
        raise ValueError("You're passing incorrect fields.")
    assert(all(package.values()) == True)

    msg = MIMEMultipart()

    for key in package:
        if key in ('to','from','subject'):
            msg[key] = package[key]

    if isinstance(package.get('recipients'), str):
        package['recipients'] = package.get('recipients').split(',')

    if message:
        msg.attach(MIMEText(message))

    if file_path:
        with open(file_path, "rb") as file:
            msg.attach(MIMEApplication(
                file.read(),
                Content_Disposition='attachment;filename="{}"'.format(os.path.basename(file_path)),
                Name=os.path.basename(file_path)
            ))

    if send:
        # read more @ https://docs.python.org/3.5/library/smtplib.html 
        # cannot use a context manager here since it requires python 3.3
        server = SMTP("smtp.gmail.com", 587)
        server.ehlo() 
        server.starttls() 
        server.login(auth.user, auth.password)
        server.sendmail(package['sender'], package['recipients'], msg.as_string())
        server.close()
    else:
        return msg









