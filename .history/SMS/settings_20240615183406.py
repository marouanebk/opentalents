"""
Django settings for SMS project.

Generated by 'django-admin startproject' using Django 3.0.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""
from django.contrib.messages import constants as messages
import os


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# images directory
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# SECURITY WARNING: keep the secret key used in production secret!
#with open('/opentalents/secret/secret_key.txt', encoding='utf8') as f:
#    SECRET_KEY = f.read().strip()
SECRET_KEY = '???'

DATABASE_PASSWORD = 'admin'

MESSAGE_TAGS = {
    messages.ERROR: 'danger',
}

ALLOWED_HOSTS = ['*']
PROTOCOLE_HOST = 'http://localhost'
# EMAIL
EMAIL_USE_TLS = True
EMAIL_HOST = 'localhost'
EMAIL_HOST_USER = 'votre_adresse@email.dz'

#En cas de volonté de stockage du mot de passe dans un fichier texte externe, utiliser la fonction ci-dessous
#with open('/opentalents/secret/email_host_password.txt', encoding='utf8') as f:
#    EMAIL_HOST_PASSWORD = f.read().strip()
EMAIL_HOST_PASSWORD='password'
EMAIL_PORT = 587

# EMAIL_ENABLED = True to activate sending emails
EMAIL_ENABLED = False

ADMINS = (
	('Admin', 'votre_admin@email.dz'),
	)


# google AGENDA parameters
SCOPES=["https://www.googleapis.com/auth/calendar"]
#GOOGLE_CLIENT_SECRET_FILE="/opentalents/secret/code_secret_client_fet.json"

# SMS PROVIDER SETTINGS
SMS_ENABLED=False
SMS_URL='https://wsp.sms-algerie.com/api/json'
SMS_API_KEY='??'
SMS_USER_KEY='??'

# Application definition

INSTALLED_APPS = [
    'scolar.apps.ScolarConfig',
    'django_tables2',
    'django_filters',
    'crispy_forms',
    'jquery',
    'bootstrap4',
    'bootstrap_datepicker_plus',
    'social_django',
    'jchart',
    'django_icons',
    'wkhtmltopdf',
     'django_ajax',
     'django_select2',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'axes',
    'django_cleanup.apps.CleanupConfig',
    'django_extensions',
    'captcha',
    'rest_framework',
]

DATE_INPUT_FORMATS = ['%d/%m/%Y']
CRISPY_TEMPLATE_PACK = 'bootstrap4'

TIME_INPUT_FORMATS = ['%I:%M %p']


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
    'axes.middleware.AxesMiddleware',
]

ROOT_URLCONF = 'SMS.urls'

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
                'django.template.context_processors.i18n',
                'social_django.context_processors.backends',    # social_django
                'social_django.context_processors.login_redirect', # social_django
		'scolar.context_processors.institution', # default context institution info 
            ],
        },
    },
]

BOOTSTRAP4 = {
    'include_jquery': True,
}

WSGI_APPLICATION = 'SMS.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#        'ATOMIC_REQUESTS':True,
#    }
	'default':{
		'ENGINE':'django.db.backends.postgresql_psycopg2',
        'NAME':'opentalents',
		'USER':'porgres',
		'PASSWORD':'root',
		'HOST':'db',
		'PORT':'5432',
	}
}

# Login
LOGIN_URL = '/accounts/login'
LOGOUT_REDIRECT_URL = '/scolar/index'
LOGIN_REDIRECT_URL = '/scolar/index'

AUTH_USER_MODEL = 'scolar.User'

AUTHENTICATION_BACKENDS = (     # enable authentication against two backends Google and Model
	'axes.backends.AxesBackend',
    'social_core.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

# social django features and auth strategy
SOCIAL_AUTH_PIPELINE = (    
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    # Associates the current social details with another user account with
    # a similar email address. Disabled by default.
    'social_core.pipeline.social_auth.associate_by_email',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
)

# Il faut créer un client google oauth pour activer l'authetification via google
SOCIAL_AUTH_STRATEGY = 'social_django.strategy.DjangoStrategy'  # new
SOCIAL_AUTH_STORAGE = 'social_django.models.DjangoStorage'  # new
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '??' # new
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '??'   # new
SOCIAL_AUTH_REDIRECT_IS_HTTPS = True
SOCIAL_AUTH_FIELDS_STORED_IN_SESSION = ['state']


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Algiers'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'root') 
STATICFILES_DIRS = [
#    os.path.join(BASE_DIR, 'static'),
#    os.path.join(BASE_DIR, 'media'),
]

# security settings
#CSRF_COOKIE_SECURE = True
#SESSION_COOKIE_SECURE = False
#SECURE_HSTS_SECONDS = 3600
#SECURE_HSTS_INCLUDE_SUBDOMAINS = True
#SECURE_SSL_HOST = 'talents.esi.dz'
#SECURE_SSL_REDIRECT = True
#SECURE_CONTENT_TYPE_NOSNIFF = True
#SECURE_BROWSER_XSS_FILTER = True
#X_FRAME_OPTIONS = 'SAMEORIGIN'
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_HTTPONLY = False
#SESSION_COOKIE_SAMESITE = None

WKHTMLTOPDF_CMD = 'xvfb-run -a wkhtmltopdf --enable-local-file-access'

#REGEX_MATRICULE='\d\d/\d\d\d\d'
REGEX_MATRICULE='[a-zA-Z0-9/]+'

from datetime import timedelta
AXES_ENABLED=True
AXES_FAILURE_LIMIT=3
AXES_LOCK_OUT_AT_FAILURE=True
AXES_COOLOFF_TIME=timedelta(minutes=15)#Nombre de minutes avant réinitialisation
AXES_LOCK_OUT_BY_COMBINATION_USER_AND_IP=True
AXES_META_PRECEDENCE_ORDER = ['HTTP_X_FORWARDED_FOR', 'REMOTE_ADDR']
AXES_RESET_ON_SUCCESS = False

DEV_MODE=False


CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://cache:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    'select2': {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://cache:6379/2",  
        "TIMEOUT":10000,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

# Set the cache backend to select2
SELECT2_CACHE_BACKEND = 'select2'


# pour pouvoir générer les schémas E/A
GRAPH_MODELS = {
	'all_applications':True,
	'group_models':True,
}


# Pour utiliser Google ReCaptcha (pour registration des étudiants si elle est activée dans les paramètres de l'institution)
RECAPTCHA_PUBLIC_KEY = '???'
RECAPTCHA_PRIVATE_KEY = '???'

DATA_UPLOAD_MAX_NUMBER_FIELDS=10000