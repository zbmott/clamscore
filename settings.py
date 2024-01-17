import os

WCL_CLIENT_ID = os.environ.get('BNET_CLIENT_ID')
WCL_CLIENT_SECRET = os.environ.get('BNET_SECRET')

try:
    from local_settings import *
except ImportError:
    pass
