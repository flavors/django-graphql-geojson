import os


DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': os.environ['POSTGRES_DB_NAME'],
        'USER': os.environ.get('POSTGRES_DB_USER', 'postgres'),
        'PASSWORD': os.environ.get('POSTGRES_DB_PASSWORD', ''),
    },
}

SECRET_KEY = 'test'
