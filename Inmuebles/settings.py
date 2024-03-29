"""
Django settings for inmuebles project.

Generated by 'django-admin startproject' using Django 5.0.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import os 
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
#SECRET_KEY = 'django-insecure-ee-rz&-gf$+r90^6=8wi^)zxp72_w@5t*q58^l_4d4p_9$g2t6'
#utilizo varible de entorno para llevarlo a producción y para esto se importa el modulo os, y luego:
SECRET_KEY = os.environ.get('SECRET_KEY', default='your secret key') #d esta forma lee la varible de entorno d la nube osea no usa la
# la clave secreta desde aquí osea desde local



#SECURITY WARNING: don't run with debug turned on in production!
#DEBUG = True
#si render no está por dirá q True ya q se cumple, pero si está dirá q False
DEBUG = 'RENDER' not in os.environ #si existe render pondrá Debug=False, sino existe RENDER entiende q esta en local y será True

ALLOWED_HOSTS = [] #acá en modo desarrolla al estar vacio quiere decir q todos podrán tener acceso

#para q si existe en la nube el valor de 'RENDER_EXTERNAL_HOSTNAME'  q lo agregué
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'inmuebleslist_app', 
    'rest_framework', 
   'rest_framework.authtoken',                        
    'user_app',
    'django_filters',
]
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
   'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]


ROOT_URLCONF = 'Inmuebles.urls'

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

WSGI_APPLICATION = 'Inmuebles.wsgi.application'


AUTH_USER_MODEL='user_app.Account'  



# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

#Configuración Postgres
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'USER': 'postgres',
#         'NAME': 'postgres',
#         'PASSWORD': '12345',
#         'HOST':'localhost'
#     }
# }
DATABASES = {
    'default': dj_database_url.config(
        default='postgresql://postgres:12345@localhost/postgres', 
        conn_max_age=600
    )
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'

#sino estamos en desarrollo osea el Debug no está en True es q es falso y estamos en producción
if not DEBUG: 
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') #el archivo 'staticfiles' se genera con un comando
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
    





# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES':[
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ], 
  
     'DEFAULT_THROTTLE_RATES':{   
        'anon':'1000/day',  
        'user':'1000/day',
        'comentario-create': '2/day',
        'comentario-list': '900/day',

        'comentario-detail': '5/day', 
        'edificacion-list': '3000/day'
     }, 
    'DEFAULT_RENDERER_CLASSES':
    ('rest_framework.renderers.JSONRenderer', 
     
    ),
}
from datetime import timedelta

SIMPLE_JWT = {
    'ROTATE_REFRESH_TOKENS':True,
    'ACCESS_TOKEN_LIFETIME':timedelta(days=365),
    'REFRESH_TOKEN_LIFTIME':timedelta(days=365),
}



