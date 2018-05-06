# -*- coding: utf-8 -*-
from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [
    'iupick.com', 
    'www.iupick.com']

CORS_ORIGIN_WHITELIST = (
    'iupick.com',
    'www.iupick.com')

STATIC_ROOT = os.path.join(BASE_DIR, "../static/")

EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = os.environ['SENDGRID_USER']
EMAIL_HOST_PASSWORD = os.environ['SENDGRID_PASSWORD']
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'iuPick noreply@iupick.com'

AUTH_SECRET_PREFIX = 'sk_live_'