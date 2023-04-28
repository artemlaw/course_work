import requests


class YandexDisk:
    def __init__(self, token: str):
        self.token = token

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }

    def put_folder(self, folder_path):
        url = 'https://cloud-api.yandex.net/v1/disk/resources'
        headers = self.get_headers()
        params = {'path': folder_path}
        response = requests.put(url, headers=headers, params=params)
        res_body = response.json()

        if 'error' in res_body:
            print('YA ERROR:', res_body['message'])

        if response.status_code == 201:
            print(f'Папка "{folder_path}" добавлена')

        response.raise_for_status()

    def post_upload(self, file_path, file_url):
        url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        headers = self.get_headers()
        params = {'path': file_path, 'url': file_url}
        res_post_upload = requests.post(url, headers=headers, params=params)
        res_body = res_post_upload.json()

        if 'error' in res_body:
            print('YA ERROR:', res_body['message'])

        if res_post_upload.status_code == 202:
            print(f'Файл "{file_path.split("/")[-1]}" записан')

        res_post_upload.raise_for_status()
