"""
Settings file for the superhero project
"""
# Django settings for superhero project.
import os
SITE_ROOT = os.path.dirname(os.path.realpath(__file__))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'dev.sqlite',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}
# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Amsterdam'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

STATIC_URL = '/collected_media/'
STATIC_ROOT = os.path.join(SITE_ROOT, 'collected_media')

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(SITE_ROOT, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'


# Make this unique, and don't share it with anybody.
SECRET_KEY = 'GENERATE_A_NEW_SECRET'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    #'debug_toolbar.middleware.DebugToolbarMiddleware',
    'social.middleware.GenusExceptionMiddleware',
)

INTERNAL_IPS = (
    )

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates"
    # or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    #os.path.join(SITE_ROOT, 'social', 'templates'),
    os.path.join(SITE_ROOT, 'customcore', 'templates'),
)
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    #'django.core.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',

    'django.contrib.messages.context_processors.messages',

    'django.core.context_processors.request',
)


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    
#    'django_extensions',
    #'debug_toolbar',   
    #'djcelery',
    'south',
    #'reversion',
    'django.contrib.staticfiles',
    'customcore',
    'social',
    'genus',
    'core',
    #'generic_confirmation',
)
AUTH_PROFILE_MODULE = 'social.ProfileInformation'

STATICFILES_DIRS = (
  SITE_ROOT + './../lib/python2.6/site-packages/admin_tools/media/',
)

CONSUMER_KEY = 'YOUR_HYVES_API_KEY'
CONSUMER_SECRET = 'YOUR_CONSUMER_SECRET'
CONSUMER_METHODS = (
    'media.getByLoggedin',
    'albums.create',
    'albums.getBuiltin',
    'media.getByAlbum',
    'users.getFriendsByLoggedinSorted',
    'users.get',
    'friends.get',
    'users.getLoggedin',
    'users.sendNotificationToFriend',
    'users.search',
    'users.searchInFriends',
    'media.getUploadToken',
    'users.updateMedia',
    'media.addTag',
    'albums.addMedia',
    'commercial.installPimp',
    )

FLOW_REDIRECT_URL = '/invalid_session/'

CONSUMER_VERSION = '2.0'

HYVES_AUTHORIZATION_URL = 'http://www.hyves.nl/api/authorize/'

# optional setting. Sets the expiration type, note that not in all flows for retrieving a valid access token this setting is used
HYVES_EXPIRATION_TYPE = 'default'

SEND_TO_FRIEND_SUBJECT = 'A test send to a friend mail'

#FRIENDS_LIST_CACHING = 60 * 5

HYVES_LIST_PAGE_SIZE = 150
