"""
# TODO: module docstrings
"""

class BasicAuth:
    """ 
    # TODO: class docstrings
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