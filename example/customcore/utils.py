from django.contrib.auth.models import User

from social.models import UserAssociation

from social.utils import get_genus

def retrieve_friends(from_user = ''):
    """Retrieve a list of friends and stores it in the cache
    (it's also returned).
    
    .. note::
      This method requires a valid access_token (UserAssociation instance).
    """

    from django.conf import settings

    user = User.objects.get(id=from_user)

    genus = get_genus()

    access_token = UserAssociation.objects.get(user = user)

    params = (
        {
            'sorttype': 'alphabetically',
            'ha_responsefields': 'profilepicture',
            'ha_resultsperpage': settings.HYVES_LIST_PAGE_SIZE,
            'ha_page': '1',
        }
    )

    method = 'users.getFriendsByLoggedinSorted'

    result = genus.do_method(method, params, access_token)

    users = result['user']

    total_pages = result['info']['totalpages']

    if result['info']['currentpage'] < total_pages:

        for i in range(2, total_pages+1):
            params = (
                {
                    'sorttype': 'alphabetically',
                    'ha_responsefields': 'profilepicture',
                    'ha_resultsperpage': settings.HYVES_LIST_PAGE_SIZE,
                    'ha_page': i,
                }
            )

            params['ha_page'] = str(i)

            result = genus.do_method(method, params, access_token)

            users.extend(result['user'])

    user_info = []
    
    for user in users:
        temp_info = {
                'userid': user['userid'],
                'firstname': user['firstname'],
                'lastname': user['lastname'],
                'friendscount': user['friendscount'],
                'profilepicture': {
                    'icon_large': {
                        'src_medium' :
                            user['profilepicture']['square_extralarge']['src'],
                        'src_small' :
                            user['profilepicture']['square_large']['src'],
                    }
                }
            }

        if user['profilepicture'].has_key('image'):
            src = user['profilepicture']['image']['src']
	else:
            src = user['profilepicture']['icon_extralarge']

        temp_info['profilepicture']['src'] = src
        user_info.append(temp_info)

    return user_info

