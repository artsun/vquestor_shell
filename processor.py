from presets import VERSION
from extractors import vk_extractor
import time


def compare(user: str, friend: str):
    user = user.split('.')
    friend = friend.split('.')
    return True if ((user[1] == friend[1]) and abs(int(user[0]) - int(friend[0])) < 5) else False


def make_success_dict(user_id:int, user_data: dict, list_of_friends:dict):
    """runs across array of friends and tries to extract id, name and bdate
    returns success dict {id: {'last_name':x, 'first_name':y, 'bdate':z}}
    """
    if not user_data[user_id].get('bdate', False):
        return {}

    success_dict = dict()
    for friend in list_of_friends['response']['items']:
        if friend.get('bdate', False):
            if compare(user_data[user_id]['bdate'], friend['bdate']):
                success_dict.update({friend['id']: {
                    'first_name': friend['first_name'], 'last_name': friend['last_name'],
                    'bdate': friend['bdate'], 'photo_50': friend['photo_50']}})
    return success_dict


def getnode(user_id: int, mytoken):
    """
    returns dict: {id:{'first_name', ...}}
    """
    node_raw = vk_extractor(mytoken, 'getUser', user_id, VERSION, 'bdate', 'photo_50')
    # frequency queries control (check key ['response'])
    if not node_raw.get('response', False):
        time.sleep(1.5)
        node_raw = vk_extractor(mytoken, 'getUser', user_id, VERSION, 'bdate', 'photo_50')

    node_raw = node_raw['response'][0]

    # availability control
    if not node_raw.get('bdate', False):
        print("Birthday in Node not available!")
        node = {user_id: {'first_name': node_raw['first_name'], 'last_name': node_raw['last_name'],
                      'photo_50': node_raw['photo_50']}}
        return node
    node = {user_id: {'first_name': node_raw['first_name'], 'last_name': node_raw['last_name'],
                  'bdate': node_raw['bdate'], 'photo_50': node_raw['photo_50']}}
    return node


def getlinks(user_id: int, user_data: dict, mytoken):
    """
    returns dict: {id:{'first_name', ...}}
    """
    list_of_friends_data = vk_extractor(mytoken, 'getFriends', user_id, VERSION, 'bdate', 'photo_50')
    # if profile is private
    if not list_of_friends_data.get('response', False):
        print("profile is private", list_of_friends_data)
        return {}
    else:
        return make_success_dict(user_id, user_data, list_of_friends_data)
