from django.conf.urls.defaults import *
from django.views.generic.base import TemplateView
from django.conf.urls.static import static

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from django.conf import settings

urlpatterns = patterns('',

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    #url(r'^admin_tools/', include('admin_tools.urls')),
    url(r'^authorized_redirect/',
        'social.views.get_user_authorized_redirect',
        name='authorized_redirect',),
    url(r'^logintoken/(?P<logintoken>.*)/',
        'social.views.get_authorization_by_logintoken'),
    url(r'^authorize/',
        'social.views.get_user_authorization',
        name='get_user_authorization'),
    url(r'^authorized', 'social.views.get_authorized', name='get_authorized',),
    url(r'^do/(?P<method>.*)/', 'social.views.do_method', name='do_method',),
    url(r'authorized_popup/', 'social.views.get_user_authorized_popup'),
    url(r'invalid_session/', 'social.views.get_invalid_session'),
    url(
        r'^friends.xml',
        'customcore.views.get_friends',
    ),
    url(r'^friends.html',
        'customcore.views.get_friends',
        {'use_xml':False},
    ),
    url(r'^media.html',
        'customcore.views.get_media',
        {'use_xml':False}
    ),
    
    url(r'^media.xml',
        'customcore.views.get_media',
    ),
    
#    (r'^sentry/', include('sentry.urls')),

    url(r'^crossdomain.xml',
        TemplateView.as_view(template_name='crossdomain.xml')),
   
    url(r'^$', 'social.views.index'),

) + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT) \
+ static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
