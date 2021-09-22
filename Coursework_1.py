import requests
import os
import json
os.chdir(r'C:\\Users\\okoz2\\PycharmProjects\\pythonProject7')

from pprint import pprint

class PhotoVK:

    def getphoto(self, id):
        with open('token.txt', 'r') as file_object:
            tokenvk = file_object.read().strip()
        url = 'https://api.vk.com/method/photos.get'
        params = {
            'owner_id': id,
            'album_id': 'profile',
            'extended': 1,
            'access_token': tokenvk,
            'v':'5.131'
        }
        data = {}
        res = requests.get(url, params=params)
        info = res.json()
        with open('data.json', 'w') as f:
            json.dump(info, f)
        data.update(res.json())

        data_list = []
        my_list = []
        for i in range(len(data['response']['items'])):
            name = data['response']['items'][i]['likes']['count']
            size = data['response']['items'][i]['sizes'][-1]['type']
            url = data['response']['items'][i]['sizes'][-1]['url']
            data_dict = ({'file_name': str(name) + '.jpg', 'size': size})
            my_dict = ({'file_name': str(name) + '.jpg', 'size': size, 'url': url})
            data_list.append(data_dict)
            my_list.append(my_dict)
        pprint(data_list)
        return my_list




if __name__ == '__main__':
    id = int(input('Введите id:'))
    # token_ya = str(input('Введите токен с Полигона Яндекс.Диска:'))
    data_photo = PhotoVK()
    result = data_photo.getphoto(id)
