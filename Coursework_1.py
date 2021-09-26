import requests
import os
import json
from time import sleep
from tqdm import tqdm, tqdm_gui, trange

os.chdir(r'C:\\Users\\okoz2\\PycharmProjects\\pythonProject7')

from pprint import pprint


class PhotoVK:

    def getphoto(self, id) -> object:
        with open('token.txt', 'r') as file_object:
            tokenvk = file_object.read().strip()
        url = 'https://api.vk.com/method/photos.get'
        params = {
            'owner_id': id,
            'album_id': 'profile',
            'extended': 1,
            'access_token': tokenvk,
            'v': '5.131'
        }
        data = {}
        res = requests.get(url, params=params)
        info = res.json()
        with open('data.json', 'w') as f:
            json.dump(info, f)
        data = res.json()

        data_list = []
        photo_list = []
        data_items = data['response']['items']
        for i in range(len(data_items)):
            name = data_items[i]['likes']['count']
            size = data_items[i]['sizes'][-1]['type']
            url = data_items[i]['sizes'][-1]['url']
            data_dict = ({'file_name': str(name) + '.jpg', 'size': size})
            my_dict = ({'file_name': str(name) + '.jpg', 'size': size, 'url': url})
            data_list.append(data_dict)
            photo_list.append(my_dict)
        pprint(data_list)
        return photo_list


class YaUploader:

    def __init__(self, token):
        self.token = token

    def get_headers(self):
        return {
            'Authorization': 'OAuth {}'.format(self.token),
            'Content-Type': 'application/json'
        }

    def upload(self, data_list):
        upload_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        headers = self.get_headers()
        for i in trange(len(data_list)):
            sleep(0.01)
            file_name = data_list[i]['file_name']
            size = data_list[i]['size']
            url = data_list[i]['url']
            params = {'path': f'{path}/{file_name}', 'url': url, 'disable_redirects': False}
            response = requests.post(url=upload_url, headers=headers, params=params)
            response.raise_for_status()
            if response.status_code == 201:
                print('Success')

    @property
    def create_path(self):
        url = 'https://cloud-api.yandex.net/v1/disk/resources'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }
        params = {'path': f'Photo id {str(id)}'}
        response = requests.put(url=url, headers=headers, params=params)
        if response.status_code == 201:
            print('Created')
        return f'Photo id {str(id)}'

if __name__ == '__main__':
    id = int(input('Введите id:'))
    # token_ya = str(input('Введите токен с Полигона Яндекс.Диска:'))
    token_ya = '....'
    data_photo = PhotoVK()
    result = data_photo.getphoto(id)
    uploader = YaUploader(token_ya)
    result = data_photo.getphoto(id)
    path = uploader.create_path
    new_result = uploader.upload(result)
