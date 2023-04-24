import requests


def get_max_size(sizes):
    # вернуть type и url
    if len(sizes) > 1:
        sizes_type = ['w', 'z', 'y', 'r', 'q', 'p', 'o', 'x', 'm', 's']
        for size_type in sizes_type:
            for size in sizes:
                if size['type'] == size_type:
                    return size
        return None
    else:
        return sizes[0]


class VK:
    def __init__(self, access_token, user_id, version='5.131'):
        self.token = access_token
        self.id = user_id
        self.version = version
        self.params = {'access_token': self.token, 'v': self.version}

    def users_info(self):
        url = 'https://api.vk.com/method/users.get'
        params = {'user_ids': self.id}
        response = requests.get(url, params={**self.params, **params})
        return response.json()

    def search_groups(self, q, sorting=0):
        """
        Параметры sort
        0 — сортировать по умолчанию (аналогично результатам поиска в полной версии сайта);
        6 — сортировать по количеству пользователей.
        """
        params = {
            'q': q,
            'sort': sorting,
            'count': 300
        }
        req = requests.get('https://api.vk.com/method/groups.search', params={**self.params, **params}).json()
        #     pprint(req)
        req = req['response']['items']
        return req

    def get_photos(self,
                   owner_id,
                   album_id='profile',
                   photo_ids=None,
                   rev=0,
                   extended=1,
                   feed_type=None,
                   feed=None,
                   photo_sizes=0,
                   count=5):
        """
            Параметр album_id:
                wall — фотографии со стены;
                profile — фотографии профиля;
                saved — сохраненные фотографии. Возвращается только с ключом доступа пользователя.
        """

        params = {
            'owner_id': owner_id,
            'album_id': album_id,
            'photo_ids': photo_ids,
            'rev': rev,
            'extended': extended,
            'feed_type': feed_type,
            'feed': feed,
            'photo_sizes': photo_sizes
        }
        url = 'https://api.vk.com/method/photos.get'

        photos = []
        offset = 0
        while count > 0:
            params['offset'] = offset
            params['count'] = min(count, 1000)
            response_part = requests.get(url=url, params={**self.params, **params}).json()
            if 'error' in response_part:
                print('VK ERROR:', response_part['error']['error_msg'])
            else:
                photos += response_part['response']['items']
            count -= min(count, 1000)
            offset += 1000

        return photos
