import requests
import logging


class YandexDisk:
    def __init__(self, token: str):
        self.token = token

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }

    def create_folder(self, folder_path):
        url = 'https://cloud-api.yandex.net/v1/disk/resources'
        headers = self.get_headers()
        params = {'path': folder_path}
        response = requests.put(url, headers=headers, params=params)
        res_body = response.json()

        if 'error' in res_body:
            logging.error(f'ЯндексДиск - {res_body["message"]}')

        if response.status_code == 201:
            logging.info(f'ЯндексДиск - Создана папка "{folder_path}"')

        response.raise_for_status()

    def upload_photos(self, file_path, file_url):
        url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        headers = self.get_headers()
        params = {'path': file_path, 'url': file_url}
        res_post_upload = requests.post(url, headers=headers, params=params)
        res_body = res_post_upload.json()

        if 'error' in res_body:
            logging.error(f'ЯндексДиск - {res_body["message"]}')

        if res_post_upload.status_code == 202:
            logging.info(f'ЯндексДиск - Файл "{file_path.split("/")[-1]}" записан')

        res_post_upload.raise_for_status()
