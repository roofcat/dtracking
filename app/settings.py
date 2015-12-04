# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '%7)c#yro&000cb_f*-dhc19@p%in)dvcq%(88-7jq7f1%lha5f'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*',]


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # app de terceros
    'appengine_toolkit',
    #'debug_toolbar',
    'rest_framework',
    'rest_framework.authtoken',
    # apps
    'autenticacion',
    'configuraciones',
    'customsearch',
    'dashboard',
    'emails',
    'empresas',
    'webhooks',
)

REST_FRAMEWORK = {
    'PAGE_SIZE': 50,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAdminUser',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ),
}

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'app.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases
if os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine'):
    # Running on production App Engine, so use a Google Cloud SQL database.
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'HOST': '/cloudsql/django-tracking:azurian-tracking',
            'NAME': 'azurian_tracking',
            'USER': 'root',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'HOST': '173.194.80.144',
            'NAME': 'azurian_tracking',
            'USER': 'azurian-tracking',
            'PASSWORD': 'Paso.1234.',
        }
    }

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'es-CL'

TIME_ZONE = 'America/Santiago'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/
if os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine'):
    STATIC_ROOT = 'static'
else:
    # comentar el staticfiles_dir para ejecutar collecstatic
    # y descomentar el static_root
    #STATIC_ROOT = 'static'
    STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)
STATIC_URL = '/static/'


""" Configuraciones de almacenamiento de archivos
    en Google Cloud Storage utilizando 'appengine_toolkit'
"""
APPENGINE_TOOLKIT = {
    "APP_YAML": os.path.join(BASE_DIR, "app.yaml"),
    "BUCKET_NAME": "django-tracking",
}

DEFAULT_FILE_STORAGE = 'appengine_toolkit.storage.GoogleCloudStorage'
#STATICFILE_STORAGE = 'appengine_toolkit.storage.GoogleCloudStorage'

# definir la url para obtener los archivos adjuntos
#MEDIA_ROOT = "storage.googleapis.com/"
MEDIA_URL = "storage.googleapis.com/"
MEDIA_ROOT = "storage.googleapis.com/"
