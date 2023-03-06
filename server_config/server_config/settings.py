
import os
import environ
from pathlib import Path
from corsheaders.defaults import default_headers

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(DEBUG=(bool, False))
environ.Env.read_env(
    env_file=os.path.join(BASE_DIR, '.env')
)
AUTH_DATA = {
    "CLIENT_ID": env('CLIENT_ID'),
    "CLIENT_SECRET": env('CLIENT_SECRET'),
    "CODE_VERIFIER": env('CODE_VERIFIER'),
    "CODE_CHALLENGE": env('CODE_CHALLENGE')
}
DATABASE_DATA = {
    "ENGINE": env('DB_ENGINE'),
    "NAME": env('DB_NAME'),
    "USER": env('DB_USER'),
    "PASSWORD": env('DB_PASSWORD'),
    "HOST": env('DB_HOST'),
    "PORT": env('DB_PORT'),
}

DEBUG = env('DEBUG')
ADMIN_USER = env('ADMIN_USER')

CRYPTO_KEY = env('CRYPTO_KEY')

SECRET_KEY = env('SECRET_KEY')

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '52.78.16.47',
                 'www.ikiningyou.com', 'api.ikiningyou.com']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'test_rest_api',
    'users',
    # OAUTH2
    'oauth2_provider',
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'oauth2_provider.middleware.OAuth2TokenMiddleware',
]
AUTHENTICATION_BACKENDS = [
    'oauth2_provider.backends.OAuth2Backend',
    'django.contrib.auth.backends.ModelBackend'
]
ROOT_URLCONF = 'server_config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'server_config', 'templates')],
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

WSGI_APPLICATION = 'server_config.wsgi.application'


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


LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'
USE_I18N = True
USE_L10N = True
USE_TZ = False


STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = []

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
    ]
}
DATABASES = {

    'default': {
        'ENGINE': DATABASE_DATA.get('ENGINE'),
        'NAME': DATABASE_DATA.get('NAME'),
        'USER': DATABASE_DATA.get('USER'),
        'PASSWORD': DATABASE_DATA.get('PASSWORD'),
        'HOST': DATABASE_DATA.get('HOST'),
        'PORT': DATABASE_DATA.get('PORT'),
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
        }
    }
}

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

AUTH_USER_MODEL = 'users.User'

LOGIN_URL = '/admin/login/'


CORS_ORIGIN_ALLOW_ALL = False
CORS_ALLOW_CREDENTIALS = True
CSRF_TRUSTED_ORIGINS = ['http://52.78.16.47:8000', 'http://127.0.0.1:3000',
                        'http://www.ikiningyou.com', 'http://api.ikiningyou.com', 'https://52.78.16.47:8000', 'https://127.0.0.1:3000', 'https://www.ikiningyou.com', 'https://api.ikiningyou.com']
CORS_ALLOW_HEADERS = list(default_headers) + ['Set-Cookie', 'withcredentials',
                                              'Access-Control-Allow-Credentials', 'access-control-allow-origin']
CORS_ALLOWED_ORIGINS = [
    'http://52.78.16.47:8000', 'http://127.0.0.1:3000',
    'http://www.ikiningyou.com', 'http://api.ikiningyou.com',
    'https://52.78.16.47:8000', 'https://127.0.0.1:3000',
    'https://www.ikiningyou.com', 'https://api.ikiningyou.com'
]
CORS_ORIGIN_WHITELIST = [
    'http://52.78.16.47:8000', 'http://127.0.0.1:3000',
    'http://www.ikiningyou.com', 'http://api.ikiningyou.com',
    'https://52.78.16.47:8000', 'https://127.0.0.1:3000',
    'https://www.ikiningyou.com', 'https://api.ikiningyou.com'
]
SESSION_COOKIE_HTTPONLY = True
OAUTH2_PROVIDER = {
    'ACCESS_TOKEN_EXPIRE_SECONDS': 60 * 120,
    'ALLOWED_REDIRECT_URI_SCHEMES': ['https'],
    'SCOPES': {'read': 'Read scope', 'write': 'Write scope', 'groups': 'Access to your groups'}
}
