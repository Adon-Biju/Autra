# This file tells Django which settings to use

from decouple import config

# Read from .env file
ENVIRONMENT = config('ENVIRONMENT', default='dev')

if ENVIRONMENT == 'prod':
    from .prod import *  # Use production settings
elif ENVIRONMENT == 'dev':
    from .dev import *   # Use development settings
else:
    from .base import *  # Use base settings