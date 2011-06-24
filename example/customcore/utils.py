import logging
import marshal
import urllib, urllib2

from django.core.cache import cache
from django.contrib.auth.models import User

from poster.encode import multipart_encode
from poster.streaminghttp import register_openers

register_openers()

from social.models import UserAssociation

logger = logging.getLogger('celery.task')

from social.utils import get_genus

def retrieve_friends(from_user = '', run_synchronous = True, force_update = False):
    """Retrieve a list of friends and stores it in the cache
    (it's also returned).
    
    .. note::
      This method requires a valid access_token (UserAssociation instance).
    """

    flattened = cache.get(str(from_user) + '_friends', None)

    if not force_update and flattened:
        return marshal.loads(flattened)

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

    total_results = result['info']['totalresults']

    if run_synchronous:

        if settings.DEBUG:
            try:
                sleep(settings.ASYNCHRONOUS_DELAY)
            except:
                pass

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

    user_dump = marshal.dumps(user_info)

    if run_synchronous or len(user_dump) == total_results:
        cache.set(
            str(from_user) + '_friends',
            user_dump,
            settings.FRIENDS_LIST_CACHING
        )

    return user_info

from social.utils import get_genus

def upload_media_item(access_token, title, image):
    
    genus = get_genus()
    
    params = {
    }
        
    result = genus.do_method(
        'media.getUploadToken',
        params,
        access_token)
    
    token = result['token']
    ip = result['ip']
    
    # Important: open the file first with open (nothing is returned),
    # but calling read without opening will result in None being returned
    # (No errors, no exceptions)!
    
    if type(image) == str or type(image) == unicode:
        image = open(image)
    else:
        image.open()
    
    params = {
        'title': title,
        'submit': 'Verstuurd',
        'file': image
    }
    
    datagen, headers = multipart_encode(params)
    url = 'http://%s/upload?token=%s' % (ip, urllib.quote_plus(token)) 
    req = urllib2.Request(url, datagen, headers)
    response = urllib2.urlopen(req)
    response = response.read()
    
    if response != 'Upload complete':
        raise NotImplementedError('Upload failure is not covered')
    
    url = 'http://%s/status?token=%s' % (ip, urllib.quote_plus(token))
    
    import json
    from time import sleep
    
    response = urllib.urlopen(url)
    data = response.read()
    data = json.loads(data)
    
    status = None

    while 1:
        for status in data['data'][token]:
            
            if  status['currentstate'] == 'error' or \
                status['currentstate'] == 'done':
                break

            if(status[status['currentstate']].has_key('endtime')):
                end_time = status[status['currentstate']]['endtime']
            else:
                end_time = status[status['currentstate']]['expected_endtime']
            sleep_time = end_time - data['currenttime'] + 0.1

            if sleep_time < 2:
                sleep_time = 2

            sleep(sleep_time)

            response = urllib.urlopen(url)
            data = json.loads(response.read())

        if  status['currentstate'] == 'done' or \
            status['currentstate'] == 'error':
            break

    if status and status['currentstate'] == 'done':
        return status['done']['mediaid']

