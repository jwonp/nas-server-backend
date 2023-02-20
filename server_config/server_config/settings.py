
import os
import environ
from pathlib import Path
from corsheaders.defaults import default_headers
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG=True
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/
env = environ.Env(DEBUG=(bool,True))
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

CRYPTO_KEY = env('CRYPTO_KEY')

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
CSRF_TRUSTED_ORIGINS = ['http://52.78.16.47:8000','http://127.0.0.1:3000','http://www.ikiningyou.com','http://api.ikiningyou.com', 'https://52.78.16.47:8000','https://127.0.0.1:3000','https://www.ikiningyou.com','https://api.ikiningyou.com']
CORS_ALLOW_HEADERS = list(default_headers) + ['Set-Cookie']
CORS_ORIGIN_WHITELIST = (
    'http://52.78.16.47:8000','http://127.0.0.1:3000',
    'http://www.ikiningyou.com','http://api.ikiningyou.com',
    'https://52.78.16.47:8000','https://127.0.0.1:3000',
    'https://www.ikiningyou.com','https://api.ikiningyou.com' 
)
SESSION_COOKIE_HTTPONLY = True
# CSRF_COOKIE_HTTPONLY = True
OAUTH2_PROVIDER = {
    'ACCESS_TOKEN_EXPIRE_SECONDS': 60 * 120,
    'ALLOWED_REDIRECT_URI_SCHEMES':['https'],
    'SCOPES' : {'read': 'Read scope', 'write':'Write scope', 'groups':'Access to your groups'}
}


DEFAULT_LOGGING = {
    # 설정이 dictConfig version 1 형식
    # 현재는 버전 하나 뿐
    'version': 1,

    # 기존의 로거들을 비활성화하지 않는다.
    # 이전 버전과의 호환성을 위한 항목
    'disable_existing_loggers': False,

    # 필터 2개 정의
    'filters': {
        # DEBUG=False인 경우만 핸들러 동작.
        'require_debug_false': {
            # 특별키 (): 필터 객체를 생성하기 위한 클래스를
            # 장고에서 별도로 정의
            '()': 'django.utils.log.RequireDebugFalse',
        },

        # DEBUG=True인 경우만 핸들러 동작
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },

    # 포맷터 1개 정의
    'formatters': {
        # 로그 생성 시각과 로그 메시지만을 출력
        'django.server': {
            # 포맷터 객체를 생성하기 위한 클래스를 별도로 정의
            '()': 'django.utils.log.ServerFormatter',
            'format': '[{server_time}] {message}',
            'style': '{',
        }
    },

    # 핸들러 3개 정의
    'handlers': {
        # INFO 레벨 및 그 이상의 메시지를 표준 에러로 출력해주는
        # StreamHandler 클래스 사용
       'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
        },

        # django.server 로거에서 이 핸들러 사용
        'django.server': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'django.server',
        },

        # ERROR 및 그 이상의 로그 메시지를 사이트 관리자에게
        # 이메일로 보내주는 AdminEmailHandler 클래스 사용
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },

    # 로거 2개 정의
    'loggers': {
        # INFO 및 그 이상의 로그 메시지를
        # console 및 mail_admins 핸들러에게 전송
        # django.* 계층. 즉, django 패키지 최상위 로거
        'django': {
            'handlers': ['console', 'mail_admins'],
            'level': 'INFO',
        },

        # INFO 레벨 및 그 이상의 메시지를
        # django.server 핸들러에게 전송
        # runserver에서 사용하는 로거
        # 5XX : EROOR, 4XX: WARNING, 그 외 INFO 메시지
        'django.server': {
            'handlers': ['django.server'],
            'level': 'INFO',
            # 상위 로거로 로그 메시지 전파하지 않는다.
            'propagate': False,
        },
    }
}