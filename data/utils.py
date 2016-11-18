"""
# TODO: module docstrings
"""
import os

from smtplib import SMTP
from data import auth
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

def send_email(package, message=None, file_path=None, host=None, port=None):
    """ Simple message, attachment or message + attachment sending from 
    an SMTP server.

    Args:
        param1 (dict): package, dictionary containing fields
        param2 (str): message, optional message to include in email
        param3 (str): file_path,  absolute filepath to attachment
        param4 (str): host, host of email server
        param5 (int): port, port of email server

        
    Returns:
        bool: The return value. True for success, False otherwise.


    Example package parameter:
        {'from': 'engineering team',
         'to': 'management team',
         'subject': 'engineering value at all time high',
         'sender': 'noblemen@engineering',
         'recipients': ['jester1@management',
                        'jester1@management']}

    """
    success = True
    keys = set(package.keys()) 
    check = set(['from','to','subject','sender','recipients'])

    if keys != check:
        raise ValueError("Make sure you have the correct fields.")
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
    
    try:
        server = SMTP(host, port)
        server.ehlo()
        server.starttls()
        server.login(auth.user, auth.password)
        server.sendmail(package['sender'], package['recipients'], msg.as_string())
        server.close()
    except Exception as error:
        print(error[1])
        success = False

    return success









