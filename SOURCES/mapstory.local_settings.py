from local_key import *
MEDIA_ROOT = '/var/lib/mapstory/media/'
#DATABASE_PASSWORD = 'foobar'
DATABASE_HOST = 'localhost'
OGC_SERVER['default']['PASSWORD'] = 'geoserverer'
OGC_SERVER['default']['PUBLIC_LOCATION'] = 'http://192.168.56.151/geoserver/'
LOCAL_CONTENT = False
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
ENABLE_SOCIAL_LOGIN = True
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
INSTALLED_APPS += MAPSTORY_APPS
