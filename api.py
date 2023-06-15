import requests
import json
from requests_toolbelt.multipart.encoder import MultipartEncoder
import os

class PetFriends:
    """апи библиотека к веб приложению Pet Friends"""
    def __init__(self):
        self.base_url = "https://petfriends.skillfactory.ru/"


# получение кдюча авторизации
    def get_api_key(self, email, password):
        """Метод делает запрос к API сервера и возвращает статус запроса и результат в формате
                JSON с уникальным ключом пользователя, найденного по указанным email и паролем"""
        headers = {
            'email': email,
            'password': password
        }
        res = requests.get(self.base_url + 'api/key', headers = headers)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text

        return status, result

# получение списка питомцев

    def get_list_of_pets(self, auth_key, filter):
        """Метод делает запрос к API сервера и возвращает статус запроса и результат в формате JSON
                со списком найденных питомцев, совпадающих с фильтром. На данный момент фильтр может иметь
                либо пустое значение - получить список всех питомцев, либо 'my_pets' - получить список
                собственных питомцев"""
        # print(auth_key)
        headers = {
            'auth_key': auth_key['key']
        }
        filter = {
            'filter': filter
        }

        # if 'key' in auth_key:
        #     res = requests.get(self.base_url + 'api/pets', headers = headers, params = filter)
        # else
        #     return res.status_code,

        # result = ""


        res = requests.get(self.base_url + 'api/pets', headers=headers, params=filter)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text

        return status, result

    def add_new_pet(self, auth_key: json, name: str, animal_type: str,
                    age: str, pet_photo: str) -> json:
        """Метод отправляет (постит) на сервер данные о добавляемом питомце и возвращает статус
        запроса на сервер и результат в формате JSON с данными добавленного питомца"""



        if os.path.isfile(pet_photo):
            data = MultipartEncoder(
                fields = {
                    'name': name,
                    'animal_type': animal_type,
                    'age': age,
                    'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
                })
        else:
            data = MultipartEncoder(
                fields = {
                    'name': name,
                    'animal_type': animal_type,
                    'age': age
                })

        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        res = requests.post(self.base_url + 'api/pets', headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        # print(result)
        return status, result

    def add_simple_pet(self, auth_key: json, name: str, animal_type: str,
                    age: str) -> json:
        """Метод отправляет (постит) на сервер данные о добавляемом питомце, без фото и возвращает статус
        запроса на сервер и результат в формате JSON с данными добавленного питомца"""

        data = MultipartEncoder(
            fields = {
                'name': name,
                'animal_type': animal_type,
                'age': age
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        res = requests.post(self.base_url + '/api/create_pet_simple', headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        # print(result)
        return status, result

    def delete_pet(self, auth_key: json, pet_id: str) -> json:
        """Метод отправляет на сервер запрос на удаление питомца по указанному ID и возвращает
        статус запроса и результат в формате JSON с текстом уведомления о успешном удалении.
        На сегодняшний день тут есть баг - в result приходит пустая строка, но status при этом = 200"""

        headers = {'auth_key': auth_key['key']}

        res = requests.delete(self.base_url + 'api/pets/' + pet_id, headers=headers)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def update_pet_photo(self, auth_key: json, pet_id: str, pet_photo: str) -> json:
        """Метод отправляет запрос на сервер об обновлении фото питомца по указанному ID и
        возвращает статус запроса и result в формате JSON с обновлёнными данными питомца"""

        # headers = {'auth_key': auth_key['key']}

        data = MultipartEncoder(
            fields = {
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}



        # data = {
        #     'pet_photo': pet_photo
        # }
        #


        res = requests.post(self.base_url + 'api/pets/set_photo/' + pet_id, headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def update_pet_info(self, auth_key: json, pet_id: str, name: str,
                        animal_type: str, age: int) -> json:
        """Метод отправляет запрос на сервер об обновлении данных питомца по указанному ID и
        возвращает статус запроса и result в формате JSON с обновлёнными данными питомца"""

        headers = {'auth_key': auth_key['key']}
        data = {
            'name': name,
            'age': age,
            'animal_type': animal_type
        }

        res = requests.put(self.base_url + 'api/pets/' + pet_id, headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result