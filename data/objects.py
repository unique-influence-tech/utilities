"""
Classes used throughout data package.
"""

class BasicAuth:
    """ The '<BasicAuth Object>' is an object that contains
    user and password properties. The idea is that this object can
    be imported into a variety of modules and they will share 
    the same credentials. It acts global without being global.

    :params user: str, user identifier
    :params password: str, password
    """
    _shared = {}

    def __init__(self, user=None, password=None):
        self.__dict__ = self._shared 
        self._user = ''
        self._password = ''
    
    def set_credentials(self, user, password):
        self._user = user
        self._password = password
    
    @property
    def user(self):
        if self._user:
            return self._user
        return False

    @property
    def password(self):
        if self._password:
            return self._password
        return False

    def __str__(self):
        if self._user and self._password:
            return '<BasicAuth Object [Signed]>'
        return '<BasicAuth Object [Unsigned]>'