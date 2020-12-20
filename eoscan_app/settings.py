import os
from .config import SECRET_KEY, DATABASES

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    # MY APPS
    'recognition',
    # OTHER
    'debug_toolbar',
    'django_celery_results',
    'captcha',
    'django_cleanup',
    'easy_thumbnails',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # OTHER
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'eoscan_app.urls'

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

WSGI_APPLICATION = 'eoscan_app.wsgi.application'

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'NumericPasswordValidator',
    },
]


# Internationalization
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

DATE_INPUT_FORMATS = ['%d-%m-%Y']


# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'
# искать статику в этих папках, пока в одной
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# хост, с которого debugtoolbar мониторит запросы
INTERNAL_IPS = [
    '127.0.0.1',
]

# login/logout
# ссылка для входа
LOGIN_URL = '/login/'
# куда направить при успешном входе
LOGIN_REDIRECT_URL = '/'
LOGOUT_URL = '/'
LOGOUT_REDIRECT_URL = '/login/'

# celery
# в рэббит работает над очередью задач
CELERY_BROKER_URL = 'amqp://localhost:5672'
# в селери базу сохраняет результаты
CELERY_RESULT_BACKEND = 'rpc://'
# CELERY_RESULT_BACKEND = 'django-db' # в селери базу сохраняет результаты
# CELERY_ACCEPT_CONTENT = ['application/json']
# CELERY_RESULT_SERIALIZER = 'json'
# CELERY_TASK_SERIALIZER = 'json'  ticfiles.finders.AppDirectoriesFinder',

# EMAIL
# в качестве письма создается файлик
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
# куда класть эти файлы
EMAIL_FILE_PATH = 'tmp/app-messages'

# CAPTCHA
CAPTCHA_CHALLENGE_FUNCT = 'captcha.helpers.random_char_challenge'
# CAPTCHA_CHALLENGE_FUNCT = 'captcha.helpers.math_challenge'
CAPTCHA_IMAGE_SIZE = (120, 50)

# UPLOAD FILES
DATA_UPLOAD_MAX_MEMORY_SIZE = 25_000_000_000

# Настройки easy_thumbnails
THUMBNAIL_ALIASES = {
    'recognition': {'default': {'size': (300, 0),'crop': 'scale'}}
}
THUMBNAIL_DEFULT_OPTIONS = {'quality': 90, 'subsampling': 1}
THUMBNAIL_MEDIA_ROOT = os.path.join(BASE_DIR, 'miniatures/')
THUMBNAIL_MEDIA_URL = '/thumbs/'
THUMBNAIL_PREFIX = 'MINI_'
THUMBNAIL_PRESERVE_EXTENSIONS = ('gif', 'png', 'jpg', 'jpeg', 'tif', 'tiff')

# для конвертации байтов в Мб
BYTES_TO_MB_COEF = 1/1024/1024

# расположение файлов весов для нейронных сетей
WEIGHT_ROOT = os.path.join(BASE_DIR, 'static', 'weights')

# MESSAGES
MESSAGE_STORAGE = 'django.contrib.messages.storage.fallback.FallbackStorage'
MESSAGE_LEVEL = 20
