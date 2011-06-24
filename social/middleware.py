from genus.exceptions import GenusTransportError

from django.views.generic.simple import direct_to_template
from django.core.signals import got_request_exception

class GenusExceptionMiddleware(object):
    """Handle the the GenusTransportError exception by rendering a simple
    page instead of a server 500/502 page (when not running in debug mode).
    
    Based on a possible use_xml kwargs it is determined if this function should
    return xml or html.
    """
    
    def process_view(self, request, view_func, view_args, view_kwargs):
        try:
            return view_func(request, *view_args, **view_kwargs)
        except GenusTransportError, e:
            from django.conf import settings
            
            if settings.DEBUG:
                raise
            else:
                
                if view_kwargs.get('use_xml', False):
                    template = 'social/epic_fail.xml'
                    mimetype = 'text/xml'
                else:
                    template = 'social/epic_fail.html'
                    mimetype = 'text/html'
                got_request_exception.send(sender = self, request = request)
                return direct_to_template(request, template, mimetype=mimetype)
