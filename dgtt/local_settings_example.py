DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'dgtt',
        'USER': 'dgtt',
        'PASSWORD': 'dgtt',
        'HOST': 'localhost',
        'PORT': '5432',
    },
}
