
import os
import environ
from pathlib import Path
from corsheaders.defaults import default_headers
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/
env = environ.Env(DEBUG=(bool,False))
environ.Env.read_env(
    env_file = os.path.join(BASE_DIR,'.env')
)
AUTH_DATA ={
    "CLIENT_ID" : env('CLIENT_ID'),
    "CLIENT_SECRET" : env('CLIENT_SECRET'),
    "CODE_VERIFIER" : env('CODE_VERIFIER')
}
DATABASE_DATA = {
    "ENGINE":env('DB_ENGINE'),
    "NAME" : env('DB_NAME'),
    "USER" : env('DB_USER'),
    "PASSWORD" : env('DB_PASSWORD'),
    "HOST" : env('DB_HOST'),
    "PORT" : env('DB_PORT'),
}

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = env('DEBUG')

ALLOWED_HOSTS = ['127.0.0.1','localhost','52.78.16.47','www.ikiningyou.com','api.ikiningyou.com']


# Application definition

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
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'oauth2_provider.middleware.OAuth2TokenMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]
AUTHENTICATION_BACKENDS = [
    'oauth2_provider.backends.OAuth2Backend',
    'django.contrib.auth.backends.ModelBackend'
]
ROOT_URLCONF = 'server_config.urls'

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

WSGI_APPLICATION = 'server_config.wsgi.application'



# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'ko-kr'
 
TIME_ZONE = 'Asia/Seoul'
USE_I18N = True
USE_L10N = True
USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
        # 'oauth2_provider.ext.rest_framework.OAuth2Authentication',
        # 'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
        
        # 'oauth2_provider.ext.rest_framework.OAuth2Authentication',
        # 'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}
DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': BASE_DIR / 'db.sqlite3',
    # }
    'default' : {
        'ENGINE' : DATABASE_DATA.get('ENGINE'),
        'NAME' : DATABASE_DATA.get('NAME'),
        'USER' : DATABASE_DATA.get('USER'),
        'PASSWORD' : DATABASE_DATA.get('PASSWORD'),
        'HOST' : DATABASE_DATA.get('HOST'),
        'PORT' : DATABASE_DATA.get('PORT'),
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
        }
    }
}

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

AUTH_USER_MODEL='users.User'

LOGIN_URL='/admin/login/'

CORS_ORIGIN_ALLOW_ALL = False
CORS_ALLOW_CREDENTIALS = True
CSRF_TRUSTED_ORIGINS = ['http://52.78.16.47:8000','http://127.0.0.1:3000','http://www.ikiningyou.com','http://api.ikiningyou.com']
CORS_ALLOW_HEADERS = list(default_headers) + ['Set-Cookie']
CORS_ORIGIN_WHITELIST = (
    'http://52.78.16.47:8000','http://127.0.0.1:3000','http://www.ikiningyou.com','http://api.ikiningyou.com'

)
SESSION_COOKIE_HTTPONLY = True
# CSRF_COOKIE_HTTPONLY = True
OAUTH2_PROVIDER = {
    'ACCESS_TOKEN_EXPIRE_SECONDS': 60 * 120,
    'SCOPES' : {'read': 'Read scope', 'write':'Write scope', 'groups':'Access to your groups'}
}
