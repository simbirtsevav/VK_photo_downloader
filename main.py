import requests
import yadisk
import json


def vk_photo(id, count):
    if count == '':
        count = 5
    with open('vk_token.txt') as f:
        TOKEN = f.read().strip()
    URL = 'https://api.vk.com/method/photos.get?'
    params = {'owner_id': id, 'access_token': TOKEN, 'v': '5.131', 'album_id': 'profile', 'count': count, 'extended': '1'}
    res = requests.get(URL, params=params).json()
    photo_dict = {}
    photo_list = []
    for photo in res['response']['items']:
        photo_type = photo['sizes'][-1]['type']
        if photo['likes']['count'] not in photo_dict:
            photo_dict[photo['likes']['count']] = photo['sizes'][-1]['url']
            count = {'file_name': (str(photo['likes']['count']) + '.jpg'),
                     'size': photo['sizes'][-1]['type']}
        else:
            photo_dict[str(photo['date'])+'_' + str(photo['likes']['count'])] = photo['sizes'][-1]['url']
            count = {'file_name': (str(str(photo['date'])+'_' + str(photo['likes']['count'])) + '.jpg'), 'size': photo['sizes'][-1]['type']}
        photo_list.append(count)
    with open('file_info.json', 'w') as f:
       json.dump(photo_list, f)
    return photo_dict


def upload_photo(dict):
    with open('yadisk_token.txt') as f:
        TOKEN = f.read().strip()

    y = yadisk.YaDisk(token=TOKEN)
    if y.is_dir('vk') == False:
        y.mkdir('vk')
    for photo in dict:
        link = dict[photo]
        dest_name = '/vk/' + str(photo)+'.jpg'
        y.upload_url(link, dest_name)
        print(f' Фотография {str(photo)}.jpg загружена')
    print('Все фотографии успешно загружены на Диск')


upload_photo(vk_photo(input('Введите id пользователя: '), input('введите количество фотографий:')))
