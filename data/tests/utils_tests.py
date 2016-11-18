"""
# TODO: module docstrings
"""
import io
import os
import unittest

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from mock import patch
from data.utils import send_email
from data.objects import BasicAuth


class MockSMTP:
    """The MockSMTP class replaces the SMTP object in the sendmail function.

    This class takes all the methods used in the sendemail function and
    replaces them with attributes/methods that return True.

    Attributes:
        id (hex): A hex object for reference.

    """

    def __init__(self, identity=hex(id('Testing'))):

        self.id = identity

        for item in ('ehlo','starttls','login','sendmail','close'):
            self.__dict__[item] = True


class MockEmail:
    """The MockEmail class builds a mock email message.
    
    This class builds an email message used to test various
    components of the email message. 

    Attributes:
        email (str): email 
        package (dict): package containing email fields
        message (MIMEText): MIMEText wrapped string 
        file_path (dict): dictionary containing mock file and path
        attachment (MIMEApplication): MIMEApplication wrapped IO object

    """

    def __init__(self, package, message=None, file_path=None):
        
        self._email = MIMEMultipart()
        self._package = package

        for key in package:
            if key in ('to','from','subject'):
                self._email[key] = self._package[key]

        if message:
            self._message = MIMEText(message) if message else None
            self._email.attach(self._message)

        if file_path:
            mock_file = file_path.get('file')
            mock_path = file_path.get('file_path')

            self._attachment = MIMEApplication(
                mock_file,
                mock_path,
                Content_Disposition='attachment;filename="{}"'.format(os.path.basename(mock_path)),
                Name=os.path.basename(mock_file)
            )
            self._email.attach(self._attachment)

    @property
    def package(self):
        return self._package
    
    @property
    def message(self):
        return self._message
    
    @property 
    def attachment(self):
        return self._attachment

    @property 
    def email(self):
        return self._email


class SendEmailTests(unittest.TestCase):

    @classmethod
    def setUp(cls):
        cls.auth = BasicAuth()
        cls.auth.set_credentials('dryrun@testing.com', 'boneDry')
        cls.test_package = {
            'from':'Test Sender', 
            'to':'Test Users',
            'subject':'Test Subject',
            'sender':'dryrun@testing.com',
            'recipients': [
                'dummy1@tester.com', 
                'dummy2@tester.com'
            ]}
        cls.test_message = 'I am a test message.'
        cls.test_file_path = '/this/is/a/fake/file.csv'
        cls.test_file = io.StringIO('This is a test file!')

    
    def test_send_email_package_has_right_fields(self):
        package = self.test_package.copy()
        del package['from']
        self.assertRaises(ValueError, send_email, package, self.test_message)
        package['from'] = 'Test Sender'
        package['testing'] = 'Invalid Field'
        self.assertRaises(ValueError, send_email, package, self.test_message)
        

    def test_send_email_package_contains_values(self):
        package = self.test_package.copy()
        package['from'] = ''
        self.assertRaises(AssertionError, send_email, package, self.test_message)


    def test_email_construction_with_message(self):
        package = self.test_package.copy()
        message = self.test_message
        check_response = MockEmail(package, message=message)
        self.assertIsNot(check_response.message, None)


    def test_email_construction_with_attachment(self):
        package = self.test_package.copy()
        file_dict = {'file':self.test_message, 'file_path':self.test_file_path}
        check_response = MockEmail(package, file_path=file_dict)
        self.assertFalse(not check_response.email.get_payload())


    @patch('data.utils.SMTP')
    def test_send_email(self, mocked_smtp):
        mocked_smtp = MockSMTP()
        package = self.test_package.copy()
        test = send_email(package, message=self.test_message, file_path=None)
        self.assertEqual(True, test)

        
if __name__ == '__main__':
    test_suites = [SendEmailTests]

    for tests in test_suites:
        suite = unittest.TestLoader().loadTestsFromTestCase(tests)
        unittest.TextTestRunner(verbosity=2).run(suite)
