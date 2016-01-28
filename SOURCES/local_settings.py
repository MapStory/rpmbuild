# -*- coding: utf-8 -*-

from kombu import Queue

SITEURL = 'https://localhost/'
DATABASE_PASSWORD = 'foobar'
DATABASE_HOST = 'localhost'
SESSION_COOKIE_DOMAIN = 'localhost'
GEOSERVER_URL = SITEURL + 'geoserver/'
OGC_SERVER['default']['PASSWORD'] = 'geoserver'
OGC_SERVER['default']['PUBLIC_LOCATION'] = GEOSERVER_URL
LOCAL_CONTENT = False
MEDIA_ROOT = '/var/lib/geonode/gunicorn/media/'
STATIC_ROOT = '/var/lib/geonode/gunicorn/static/'
SECRET_KEY = 'XwlsDVQzAgqBYK8pmVROlyQOryVcqYd8'

if DATABASE_PASSWORD:
    GEOGIG_DATASTORE_NAME = 'geogig'
    OGC_SERVER['default']['GEOGIG_DATASTORE_DIR'] = '/var/lib/geoserver_data/geogig'

DEBUG = True

HAYSTACK_SEARCH = True
# Avoid permissions prefiltering
SKIP_PERMS_FILTER = False
# Update facet counts from Haystack
HAYSTACK_FACET_COUNTS = False
HAYSTACK_CONNECTIONS = {
   'default': {
       'ENGINE': 'mapstory.search.elasticsearch_backend.MapStoryElasticsearchSearchEngine',
       'URL': 'http://127.0.0.1:9200/',
       'INDEX_NAME': 'geonode',
       },
   }
SKIP_PERMS_FILTER = True
HAYSTACK_SIGNAL_PROCESSOR = 'mapstory.search.signals.RealtimeSignalProcessor'


MAPSTORY_APPS = (

 'mapstory.apps.boxes',
 'mapstory.apps.flag', # - temporarily using this instead of the flag app for django because they need to use AUTH_USER_MODEL

)


# Social Authentication Settings

ENABLE_SOCIAL_LOGIN = False
TWITTER_CONSUMER_KEY = 'None'
TWITTER_CONSUMER_SECRET = 'None'

FACEBOOK_APP_ID = 'None'
FACEBOOK_API_SECRET = 'None'
FACEBOOK_EXTENDED_PERMISSIONS = ['email']

GOOGLE_OAUTH2_CLIENT_ID = 'None'
GOOGLE_OAUTH2_CLIENT_SECRET = 'None'

# Registration Settings

REGISTRATION_OPEN = True
ACCOUNT_OPEN_SIGNUP = True
ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = "auth_login"
ACCOUNT_EMAIL_CONFIRMATION_REQUIRED = None
ACCOUNT_ACTIVATION_DAYS = 0
DEFAULT_FROM_EMAIL = 'None'

# Google Analytics Settings

GOOGLE_ANALYTICS = 'None'

# Email Settings

EMAIL_HOST = 'None'
EMAIL_HOST_USER = 'None'
EMAIL_HOST_PASSWORD = 'None'
EMAIL_PORT = None
EMAIL_USE_TLS = None
EMAIL_BACKEND = "mailer.backend.DbBackend"

# Slack Settings

SLACK_BACKEND = 'django_slack.backends.RequestsBackend'
SLACK_TOKEN = 'None'
SLACK_CHANNEL = 'None'
SLACK_ICON_EMOJI = 'None'
SLACK_USERNAME = 'None'


# AWS S3 Settings

USE_AWS_S3 = False

AWS_STORAGE_BUCKET_NAME = 'None'
AWS_ACCESS_KEY_ID = 'None'
AWS_SECRET_ACCESS_KEY = 'None'

INSTALLED_APPS += MAPSTORY_APPS

# Celery and RabbitMQ Settings

BROKER_URL = "amqp://mapstory:password@localhost/mapstory"

CELERY_DEFAULT_QUEUE = "default"
CELERY_DEFAULT_EXCHANGE = "default"
CELERY_DEFAULT_EXCHANGE_TYPE = "direct"
CELERY_DEFAULT_ROUTING_KEY = "default"
CELERY_CREATE_MISSING_QUEUES = True

CELERY_ALWAYS_EAGER = False  # False makes tasks run asynchronously

CELERY_RESULT_BACKEND = 'djcelery.backends.database:DatabaseBackend'
CELERY_IGNORE_RESULT=False

CELERY_EAGER_PROPAGATES_EXCEPTIONS = True