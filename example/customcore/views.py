import math

from django.shortcuts import render

from social.decorators import accesstoken_required
from customcore.utils import retrieve_friends


@accesstoken_required
def get_friends(request, genus=None, access_token=None, use_xml=True):

    """Retrieve friends list
    """

    page = request.GET.get('p', 1)
    page_size = int(request.GET.get('s', '5'))
    search = request.GET.get('search', None)

    if not use_xml:
        content_type = 'text/html'
        tmplt_file = 'customcore/get_friends.html'
    else:
        content_type = 'text/xml'
        tmplt_file = 'customcore/get_friends.xml'

    context = {}

    friends_list = retrieve_friends(
        access_token.user_id,
        run_synchronous=True,
    )

    if not search:
        relevant_friends = friends_list
    else:
        relevant_friends = []
        search = search.lower()

        for friend in friends_list:
            if friend['firstname'].lower().find(search) == 0:
                relevant_friends.append(friend)
    response = {'user': relevant_friends, 'info': {
        'page_size': page_size,
        'totalpages': int(math.ceil(len(relevant_friends) / float(page_size))),
        'currentpage': page,
        'totalresults': len(relevant_friends),
        }}

    context.update(
        {
            'users': response['user'],
            'paging': response['info'],
        }
    )

    return render(
        request,
        tmplt_file,
        context,
        content_type=content_type,
    )


@accesstoken_required
def get_media(request, genus=None, access_token=None, use_xml=True):
    """Retrieve all media items (keeping in mind the paging).
    """

    if use_xml:
        tmplt_file = 'customcore/get_media.xml'
        content_type = 'text/xml'
    else:
        tmplt_file = 'customcore/get_media.html'
        content_type = 'text/html'

    context = {}

    params = {
        'ha_resultsperpage': request.GET.get('s', '2'),
        'ha_page': request.GET.get('p', 1)
    }

    result = genus.do_method(
        'media.getByLoggedin',
        params,
        access_token
    )

    context.update(
        {
            'media': result['media'],
            'paging': result['info'],
        }
    )

    return render(
        request,
        tmplt_file,
        context,
        content_type=content_type,
    )
