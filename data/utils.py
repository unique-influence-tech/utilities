"""A set of utility functions written in Python.

This module doesn't really have a proper home yet, but my intention is for it to be 
a set of tools more people use in the future.

Example:
    
     >> import utils
     >> utils.send_email()
     >> exit()

Attributes:

    Coming Soon

Todo:

    Coming Soon
"""
import os
import io
import email
import ftplib

from smtplib import SMTP
from imaplib import IMAP4_SSL
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

def send_email(package, message=None, file_path=None, host=None, port=None):
    """ Simple message, attachment or message + attachment sending from 
    an SMTP server.

    Usage:
        >> import utils
        >> utils.send_email()
        >> exit()

    Args:
        param1 (dict): package, dictionary containing fields
        param2 (str): message, optional message to include in email
        param3 (str): file_path,  absolute filepath to attachment
        param4 (str): host, host of email server
        param5 (int): port, port of email server

    Returns:
        bool: The return value. True for success, False otherwise.

    Refs:
        None

    Example package parameter:
        {'from': 'Engineering,
         'to': 'Management',
         'subject': 'System Uptime',
         'sender': 'engineering@company.com',
         'recipients': ['manager1@company.com','manager2@company.com']}

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
        print('Error: '+error[1])
        success = False

    return success

def get_imap_attachment(account, pass_, email_, file):
    """Get chronologically latest mail attachment 
    based on exact email address and exact attachment name. 
    
    Usage:
        >>> import utils
        >>> utils.get_imap_attachment('email@domain.com', 'report')

    Args:

        param1 (str): account, receiver email
        param2 (str): pass_, password
        param3 (str): email, sender email 
        param4 (str): file, attachment phrase

    Returns:
        io.BytesIO object

    Refs:
        1: http://stackoverflow.com/questions/28584992
    """
    with IMAP4_SSL('imap.gmail.com') as server:
        # login
        server.login(account, pass_)
        server.select('Inbox')
        # filter & reorder
        resp = server.search(None, 'FROM', email_)
        raw = resp[1]
        email_ids = raw[0].split()
        email_ids.reverse()
        # traverse emails 
        for message in email_ids:
            fetch = server.fetch(message, '(RFC822)')
            assert(fetch[0] == 'OK')
            raw = fetch[1][0][1].decode('utf-8') # (1)
            mail = email.message_from_string(raw)
            for part in mail.walk():
                filename = part.get_filename()
                disposition = part.get('Content-Disposition')
                print(filename)
                if disposition is None:
                    continue
                if file.lower() in filename.lower():
                    file_obj = io.BytesIO()
                    file_obj.write(part.get_payload(decode=True))                
                    return file_obj

    return None
     
    

def get_ftp_file(user, pass_, host, dir_, file):
    """Connect to ftp host and download specified file
    providing user, password and ftp directory where file
    is located.
        
    Usage:
        >>> import utils
        >>> get_file_ftp_file('dev1', 'L33t', 'ftp.fakehost.com', 'teest', 'h4x.py')

    Args:
        param1 (str): user, username
        param2 (str): pass_, password
        param3 (str): host, ftp hostname
        param4 (str): dir_, ftp directory
        param5 (str): file, file name

    Returns:
        io.BytesIO obj

    Refs:
        None
    """
    with ftplib.FTP(host) as ftp:
        ftp.login(user, pass_)
        ftp.cwd(dir_)
        for name in ftp.nlst():
            if file.lower() == name.lower():
                file_obj = io.BytesIO()
                ftp.retrbinary('RETR {file}'.format(file=name), file_obj.write)
                break
    ftp.close()

    return file_obj








