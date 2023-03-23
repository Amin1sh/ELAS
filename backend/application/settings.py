import os
from datetime import timedelta

JWT_SECRET_KEY = 'secret'
JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=30)
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
