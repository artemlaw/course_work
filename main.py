import os
import datetime
import json
import logging
from dotenv import load_dotenv
from vk import VK, get_max_size
from ya_disk import YandexDisk


def main():
    load_dotenv()

    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

    vk_access_token = os.getenv('VK_ACCESS_TOKEN')

    if not vk_access_token:
        logging.error('Токен VK не указан. Внесите значение в файл env.')
    else:
        input_config = {
            'vk_user_id': None,
            'vk_album_id': None,
            'vk_photos_count': None,
            'ya_disk_token': None
        }

        while True:
            input_config['vk_user_id'] = str(input('Введите id пользователя VK: ')) or os.getenv('VK_USER_ID')
            if not input_config['vk_user_id']:
                logging.warning('Id пользователя не может быть пустым. Повторите ввод.')
                continue
            input_config['vk_album_id'] = input('Введите id альбома VK для резерва (по умолчанию "profile"): ') or 'profile'
            input_config['vk_photos_count'] = int(input('Введите количество фото для резерва (по умолчанию 5): ') or 5)
            input_config['ya_disk_token'] = input("Введите токен ЯндексДиск: ") or os.getenv('YA_DISK_TOKEN')
            if not input_config['ya_disk_token']:
                logging.warning('Токен ЯндексДиска не может быть пустым. Повторите ввод.')
                continue
            break

        vk = VK(vk_access_token)
        ya = YandexDisk(input_config['ya_disk_token'])
        vk_backup_photos = []
        logging.info(f'Пользователь: {input_config["vk_user_id"]}, '
                     f'альбом: {input_config["vk_album_id"]}, '
                     f'фото: {input_config["vk_photos_count"]}')
        photos = vk.get_photos(owner_id=input_config['vk_user_id'],
                               album_id=input_config['vk_album_id'],
                               count=input_config['vk_photos_count'])
        if len(photos) > 0:
            logging.info(f'VK - Получено фотографий - {len(photos)}')
            folder_name = f'vk_backup_photos_{datetime.datetime.now().strftime("%y_%m_%d_%H_%M_%S")}'
            ya.create_folder(folder_name)

            for photo in photos:
                for file in vk_backup_photos:
                    if file['file_name'] == f'{photo["likes"]["count"]}.jpg':
                        vk_backup_photos.append({'file_name': f'{photo["likes"]["count"]}_{photo["date"]}.jpg',
                                                 'size': get_max_size(photo['sizes'])['type']
                                                 })
                        ya.upload_photos(f'{folder_name}/{photo["likes"]["count"]}_{photo["date"]}.jpg',
                                         get_max_size(photo['sizes'])['url'])
                        break
                else:
                    vk_backup_photos.append({'file_name': f'{photo["likes"]["count"]}.jpg',
                                             'size': get_max_size(photo['sizes'])['type']
                                             })
                    ya.upload_photos(f'{folder_name}/{photo["likes"]["count"]}.jpg',
                                     get_max_size(photo['sizes'])['url'])

            if not os.path.exists('temp'):
                os.makedirs('temp')

            with open('temp/vk_backup_photos.json', 'w') as f:
                json.dump(vk_backup_photos, f, ensure_ascii=False, indent=4)
                logging.info('Результат с информацией по фотографиям записан в файл "vk_backup_photos.json"')

        else:
            logging.warning('По указанным параметрам фотографии не найдены или недоступны')


if __name__ == '__main__':

    '''
    Укажите системные переменные в файле .env:       
    VK_ACCESS_TOKEN - токен доступа приложения VK  
        
    Необязательные переменные, применяемые по умолчанию:
    VK_USER_ID - id пользователя резервную копию фотографии которого необходимо записать
    YA_DISK_TOKEN - токен доступа к ЯндексДиск
    
    '''

    main()
