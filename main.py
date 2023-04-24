import os
from pprint import pprint
from dotenv import load_dotenv
from vk import VK, get_max_size


def main():
    final_json = []
    photos = vk.get_photos('1', album_id='profile', count=5)

    # pprint(photos)
    for photo in photos:
        # print(f'file_name: {photo["likes"]["count"]} {photo["date"]} url: {get_max_size(photo["sizes"])}')

        for file in final_json:
            if file["file_name"] == f'{photo["likes"]["count"]}.jpg':
                final_json.append({'file_name': f'{photo["likes"]["count"]}_{photo["date"]}.jpg',
                                   "size": get_max_size(photo["sizes"])["type"]
                                   })
                break
        else:
            final_json.append({'file_name': f'{photo["likes"]["count"]}.jpg',
                               "size": get_max_size(photo["sizes"])["type"]
                               })

    pprint(final_json)


if __name__ == '__main__':
    # Входящие параметры от пользователя:
    load_dotenv()

    VK_USER_ID = os.getenv('VK_USER_ID')

    # Системные параметры
    VK_ACCESS_TOKEN = os.getenv('VK_ACCESS_TOKEN')
    YA_DISK_TOKEN = os.getenv('YA_DISK_TOKEN')
    # backup_foto_user()
    vk = VK(VK_ACCESS_TOKEN, VK_USER_ID)

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
