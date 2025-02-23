from .base import *

# DATABASES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env.str('POSTGRES_DB', default='postgres'),
        'USER': env.str('POSTGRES_USER', default='postgres'),
        'PASSWORD': env.str('POSTGRES_PASSWORD', default='postgres'),
        'HOST': env.str('POSTGRES_HOST', default='postgres'),
        'PORT': env.str('POSTGRES_PORT', default='5432'),
        'ATOMIC_REQUESTS': True,
        'OPTIONS': {},
    },
}
