import os
import datetime
import json
from dotenv import load_dotenv
from vk import VK, get_max_size
from ya_disk import YandexDisk


def main():
    vk_backup_photos = []
    photos = vk.get_photos('1', album_id='profile', count=5)
    folder_name = f'vk_backup_photos_{datetime.datetime.now().strftime("%y_%m_%d_%H_%M_%S")}'
    ya.put_folder(folder_name)

    for photo in photos:
        for file in vk_backup_photos:
            if file['file_name'] == f'{photo["likes"]["count"]}.jpg':
                vk_backup_photos.append({'file_name': f'{photo["likes"]["count"]}_{photo["date"]}.jpg',
                                         'size': get_max_size(photo['sizes'])['type']
                                         })
                ya.post_upload(f'{folder_name}/{photo["likes"]["count"]}_{photo["date"]}.jpg',
                               get_max_size(photo['sizes'])['url'])
                print(f'{photo["likes"]["count"]}_{photo["date"]}.jpg', get_max_size(photo['sizes'])['url'])
                break
        else:
            vk_backup_photos.append({'file_name': f'{photo["likes"]["count"]}.jpg',
                                     'size': get_max_size(photo['sizes'])['type']
                                     })
            ya.post_upload(f'{folder_name}/{photo["likes"]["count"]}.jpg', get_max_size(photo['sizes'])['url'])
            print(f'{photo["likes"]["count"]}.jpg', get_max_size(photo['sizes'])['url'])

    with open('temp/vk_backup_photos.json', 'w') as f:
        json.dump(vk_backup_photos, f, ensure_ascii=False, indent=4)
        print('Файл "vk_backup_photos.json" записан')


if __name__ == '__main__':
    # Входящие параметры от пользователя:
    load_dotenv()

    VK_USER_ID = os.getenv('VK_USER_ID')

    # Системные параметры
    VK_ACCESS_TOKEN = os.getenv('VK_ACCESS_TOKEN')
    YA_DISK_TOKEN = os.getenv('YA_DISK_TOKEN')
    # backup_foto_user()
    vk = VK(VK_ACCESS_TOKEN, VK_USER_ID)

    ya = YandexDisk(YA_DISK_TOKEN)

    # pprint(vk.users_info())
    # pprint(vk.search_groups('python'))

    # album_id - определенный альбом
    # возможно прикрутить получение списка альбомов
    # для реализации требования
    # - Сохранять фотографии и из других альбомов.
    # pprint(vk.get_photos('1', album_id='profile', count=5))

    # pprint(album)
    # pprint(get_max_size(album))
    main()
