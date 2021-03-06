try:
    from functools import wraps
except ImportError:
    from django.utils.functional import wraps  # Python 2.4 fallback

import pickle

from django.contrib.auth import REDIRECT_FIELD_NAME
from django.http import HttpResponseRedirect
from django.utils.http import urlquote

from social.models import UserAssociation
from social.utils import get_genus


def requesttoken_required(
        view_func,
        redirect_url=None,
        redirect_field_name=REDIRECT_FIELD_NAME):

    """Checks for 'requesttoken' in session and redirects to redirect_url (or
    settings.FLOW_REDIRECT_URL).

    It also adds request_token and genus to the kwargs of the view_func
    """

    if not redirect_url:
        from django.conf import settings
        redirect_url = settings.FLOW_REDIRECT_URL

    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):

        if request.session.get('requesttoken_user', False):

            kwargs.update(
                {
                    'requesttoken_user': pickle.loads(
                            request.session.get('requesttoken_user')
                        ),
                    'genus': get_genus()
                }
            )

            return view_func(request, *args, **kwargs)

        path = urlquote(request.get_full_path())
        tup = redirect_url, redirect_field_name, path

        return HttpResponseRedirect('%s?%s=%s' % tup)

    return _wrapped_view


def accesstoken_required(
        view_func,
        redirect_url=None,
        redirect_field_name=REDIRECT_FIELD_NAME):
    """Checks for 'accesstoken' in session and redirects to redirect_url (or
    settings.FLOW_REDIRECT_URL)

    It also adds access_token and genus to the kwargs of the view_func
    """

    if not redirect_url:
        from django.conf import settings
        redirect_url = settings.FLOW_REDIRECT_URL

    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):

        if request.user.is_authenticated():
            try:
                access_token = UserAssociation.objects.select_related().get(
                        user=request.user
                    )
            except UserAssociation.DoesNotExist:
                access_token = None

            if access_token:
                kwargs.update(
                    {
                        'access_token': access_token,
                        'genus': get_genus()
                    }
                )

                return view_func(request, *args, **kwargs)

        path = urlquote(request.get_full_path())
        tup = redirect_url, redirect_field_name, path

        return HttpResponseRedirect('%s?%s=%s' % tup)

    return _wrapped_view
