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
            response_part = requests.get(url=url, params={**self.params, **params})
            res_body = response_part.json()

            if 'error' in res_body:
                print('VK ERROR:', res_body['error']['error_msg'])
            else:
                photos += res_body['response']['items']

            response_part.raise_for_status()

            count -= min(count, 1000)
            offset += 1000

        return photos
