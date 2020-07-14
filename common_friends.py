import requests as req
from pprint import pprint

# OAUTH = 'https://oauth.vk.com/authorize'
# APP_ID = 7534966
ACCESS_TOKEN = ''
BASE_URL = 'https://api.vk.com/method/'


class User():

    def __init__(self, token, user_id):
        self.token = token
        self.user_id = user_id

    def __repr__(self):
        return f'https://vk.com/id{str(self.user_id)}'

    def __and__(self, other):
        return get_common_friends(self.user_id, other.user_id)

    def get_params(self):
        return {
            'access_token': self.token,
            'v': 5.21
        }

    def get_friends(self, user_id):
        params = self.get_params()
        params['user_id'] = user_id
        users_friends = req.get(f'{BASE_URL}/friends.get', params).json()
        for users_in_friends_list in users_friends['response']['items']:
            yield User(self.token, users_in_friends_list)

    def get_common_friends(self, initial_user_id, target_user_id):
        initial_user_friends_set = set()
        target_user_friends_set = set()
        common_friends = []
        for initial_user_friends in self.get_friends(initial_user_id):
            initial_user_friends_set.add(initial_user_friends.user_id)
        for target_user_friends in self.get_friends(target_user_id):
            target_user_friends_set.add(target_user_friends.user_id)
        for common_friend in list(initial_user_friends_set.intersection(target_user_friends_set)):
            common_friends.append(User(self.token, common_friend))
        return common_friends


user1 = User(ACCESS_TOKEN, 552934290)
user2 = User(ACCESS_TOKEN, 551055895)
pprint(user1.get_common_friends(552934290, 551055895))
