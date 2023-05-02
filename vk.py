import requests
import logging


def get_max_size(sizes):
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
    def __init__(self, access_token, version='5.131'):
        self.token = access_token
        self.version = version
        self.params = {'access_token': self.token, 'v': self.version}

    def get_photos(self,
                   owner_id,
                   album_id='profile',
                   photo_ids=None,
                   rev=1,
                   extended=1,
                   feed_type=None,
                   feed=None,
                   photo_sizes=0,
                   count=5):

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

        logging.info('VK - Начало работы с методом photos.get')

        photos = []
        offset = 0
        while count > 0:
            params['offset'] = offset
            params['count'] = min(count, 1000)
            response_part = requests.get(url=url, params={**self.params, **params})
            res_body = response_part.json()

            if 'error' in res_body:
                logging.error(f'VK - {res_body["error"]["error_msg"]}')
            else:
                photos += res_body['response']['items']
                logging.info(f'VK - Статус ответа {response_part.status_code}')

            response_part.raise_for_status()

            count -= min(count, 1000)
            offset += 1000

        return photos
