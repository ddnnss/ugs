import os
import settings

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


SECRET_KEY = 'i^tysm+*3-idq7b#rf0%b)_dv_dsuvba*^g*!jg#$f3qa6^m65'


DEBUG = True
APPEND_SLASH = True
ALLOWED_HOSTS = ['*']
AUTH_USER_MODEL = 'customuser.User'
CKEDITOR_BASEPATH = "/static/ckeditor/ckeditor/"
CKEDITOR_UPLOAD_PATH = "uploads/"

EMAIL_HOST = settings.SMTP_HOST
EMAIL_HOST_USER = settings.SMTP_LOGIN
EMAIL_HOST_PASSWORD = settings.SMTP_PASSWORD
EMAIL_PORT = settings.SMTP_PORT
EMAIL_USE_TLS = True

SOCIAL_AUTH_VK_OAUTH2_KEY = settings.VK_CLIENT_ID
SOCIAL_AUTH_VK_OAUTH2_SECRET = settings.VK_CLIENT_SECRET

"""mail ru setings"""
SOCIAL_AUTH_MAILRU_OAUTH2_KEY = settings.MAIL_ID
SOCIAL_AUTH_MAILRU_OAUTH2_SECRET = settings.MAIL_SECRET

SOCIAL_AUTH_FACEBOOK_KEY = settings.FACEBOOK_KEY
SOCIAL_AUTH_FACEBOOK_SECRET = settings.FACEBOOK_SECRET
SOCIAL_AUTH_FACEBOOK_API_VERSION = '2.4'
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
    'fields': 'id,name,email',
}

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = settings.YT_CLIENT_ID
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = settings.YT_CLIENT_SECRET

LOGIN_URL = '/'
LOGIN_REDIRECT_URL = '/'

SOCIAL_AUTH_VK_OAUTH2_SCOPE = ['email']

SOCIAL_AUTH_PIPELINE = (
    # Get the information we can about the user and return it in a simple
    # format to create the user instance later. On some cases the details are
    # already part of the auth response from the provider, but sometimes this
    # could hit a provider API.
    'social_core.pipeline.social_auth.social_details',

    # Get the social uid from whichever service we're authing thru. The uid is
    # the unique identifier of the given user in the provider.
    'social_core.pipeline.social_auth.social_uid',

    # Verifies that the current auth process is valid within the current
    # project, this is where emails and domains whitelists are applied (if
    # defined).
    'social_core.pipeline.social_auth.auth_allowed',

    # Checks if the current social-account is already associated in the site.
    'social_core.pipeline.social_auth.social_user',

    # # If there already is an account with the given steamid, pass it on to the pipeline
    # 'authentication.pipeline.associate_existing_user',
    #
    # # The username for the account is always the steamid
    # # 'social_core.pipeline.user.get_username', # Function to get the username was changed
    # 'authentication.pipeline.get_username',

    # Send a validation email to the user to verify its email address.
    # Disabled by default.
    # 'social_core.pipeline.mail.mail_validation',

    # Associates the current social details with another user account with
    # a similar email address. Disabled by default.
    # 'social_core.pipeline.social_auth.associate_by_email',

    # Create a user account if we haven't found one yet.
    'social_core.pipeline.user.create_user',

    # Create the record that associates the social account with the user.
    'social_core.pipeline.social_auth.associate_user',

    # Populate the extra_data field in the social record with the values
    # specified by settings (and the default ones like access_token, etc).
    'social_core.pipeline.social_auth.load_extra_data',

    # # Update the user record with any changed info from the auth service.
    # # 'social_core.pipeline.user.user_details',
    # # Use a custom function for this, since the details are provided separately
    'social_core.pipeline.user.user_details',
)

if not DEBUG:
    SECURE_SSL_REDIRECT = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

AUTHENTICATION_BACKENDS = (
    'social_core.backends.vk.VKOAuth2',
    'social_core.backends.mailru.MailruOAuth2',
    'social_core.backends.facebook.FacebookOAuth2',
    'social_core.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend'
)

INSTALLED_APPS = [
    'django.contrib.sitemaps',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social_django',
    'ckeditor',
    'ckeditor_uploader',

    'pages',
    'customuser',
    'cp',
    'blog'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ugs.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'customuser.context_processors.check_profile',
            ],
        },
    },
]

WSGI_APPLICATION = 'ugs.wsgi.application'



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}



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


LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = False

USE_TZ = True



STATIC_URL = '/static/'

if DEBUG:
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, "static"),
    ]
else:
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
