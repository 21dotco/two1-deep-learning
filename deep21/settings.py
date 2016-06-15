"""
Django settings for deep21 project.
"""

import os
import dotenv
import dj_database_url
from two1.wallet import Two1Wallet


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

dotenv_file = os.path.join(BASE_DIR, ".env")
if os.path.isfile(dotenv_file):
    dotenv.load_dotenv(dotenv_file)

'''
  Project-specific env vars
'''

# AWS access keys
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")

# imgur access keys
IMGUR_CLIENT_ID = os.environ.get("IMGUR_CLIENT_ID")
IMGUR_CLIENT_SECRET = os.environ.get("IMGUR_CLIENT_SECRET")

# EC2 instance configuration keys
S3_BUCKET_NAME = os.environ.get("S3_BUCKET_NAME")
EC2_SSH_KEYPAIR_ID = os.environ.get("EC2_SSH_KEYPAIR_ID")
EC2_SECURITY_GROUP_NAME = os.environ.get("EC2_SECURITY_GROUP_NAME")
EC2_IAM_INSTANCE_PROFILE_ARN = os.environ.get("EC2_IAM_INSTANCE_PROFILE_ARN")
EC2_MAX_NUM_INSTANCES = int(os.environ.get("EC2_MAX_NUM_INSTANCES", '1'))

# if you change the default region or the custom AMI, you may
# need to change/set these config variables.
EC2_AMI_ID = os.environ.get("EC2_AMI_ID", 'ami-1ab24377')
EC2_INSTANCE_TYPE = os.environ.get("EC2_INSTANCE_TYPE", 'g2.2xlarge')
AWS_DEFAULT_REGION = os.environ.get("AWS_DEFAULT_REGION", 'us-east-1')

CONTENT_SUFFIX = 'content'
STYLE_SUFFIX = 'style'
OUTPUT_SUFFIX = 'output'

BUY_PRICE = int(os.environ.get('BUY_PRICE', '125000'))
HASHIDS_SALT = os.environ.get("HASHIDS_SALT")
TMP_DIR = os.environ.get("TMP_DIR", '/tmp/')

DEBUG = os.environ.get("DEBUG", "False").lower() in ['true', 't', '1']

'''
    21 settings
'''

TWO1_WALLET_MNEMONIC = os.environ.get("TWO1_WALLET_MNEMONIC")
TWO1_USERNAME = os.environ.get("TWO1_USERNAME")
WALLET = Two1Wallet.import_from_mnemonic(mnemonic=TWO1_WALLET_MNEMONIC)

'''
    Django settings
'''

APPEND_SLASH = False
SECRET_KEY = 'not-used'

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'two1.bitserv.django',
    'deep21',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'deep21.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'deep21.wsgi.application'

# Database
DATABASES = {}
DATABASES['default'] = dj_database_url.config(conn_max_age=600)

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'
