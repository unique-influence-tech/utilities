"""
"""
from .objects import BasicAuth

auth = BasicAuth() #must instantiate auth object before utilities

from .utils import send_email

# namespace clean up 
del objects
del utils
