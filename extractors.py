import requests


def vk_extractor(mytoken='', method='', user_id='', vers=5.52, *fields):
    """
    returns json (class dict in Py)
     {'response': {'count': x, 'items': [{'': z,}{'': y,}]}}
    """
    base_url = 'https://api.vk.com/method/execute.'
    fields = ','.join([field for field in fields])
    return requests.get('%(url)s%(method)s?&v=%(version)s&fields=%(fields)s&user_id=%(id)s&access_token=%(token)s'
                        % {'url': base_url, 'method': method, 'version': vers,
                           'fields': fields, 'id': user_id, 'token': mytoken}
                        ).json()
