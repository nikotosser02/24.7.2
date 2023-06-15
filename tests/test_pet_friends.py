from api import PetFriends
from settings import valid_email, valid_password, invalid_email, invalid_password, invalid_auth_key
import os

pf = PetFriends()

def test_get_api_key_for_valid_user(email = valid_email, password = valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в результате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result


def test_get_api_key_for_invalid_user(email = invalid_email, password = invalid_password):
    """ Проверяем что запрос api ключа возвращает статус 403 и в результате не содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403
    assert 'key' not in result


def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этот ключ
    запрашиваем список всех питомцев и проверяем что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0

def test_get_all_pets_with_invalid_user(filter=''):
    """ Проверяем запрос всех питомцев, после запроса auth_key с невалидными логин/пасс возвращает статус 403
   Доступное значение параметра filter - 'my_pets' либо '' """

    status_auth, auth_key = pf.get_api_key(invalid_email, invalid_password)
    # assert status == 403
    if status_auth == 403:
        print("\nКлюч невалидный, пытаемся сделать запрос питомцев")
        # try:
        status, result = pf.get_list_of_pets(invalid_auth_key, filter)
        # except:
        # print("Запрос не удался")
        # print(status, result)
    else:
        print("Невалидный ключ принят, идет запрос")
        status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 403
    assert 'pets' not in result


def test_get_all_pets_with_invalid_key(filter=''):
    """ Проверяем запрос всех питомцев с невалидным auth_key и возвращает статус 403.
    Переменная auth_key сразу берется невалидная, не запрашивается методом получения по логин/пас.
    Доступное значение параметра filter - 'my_pets' либо '' """

    auth_key = invalid_auth_key


    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 403
    assert 'pets' not in result


def test_add_simple_pet_with_valid_data(name='Жулик', animal_type='Овчарка',
                                     age='2'):
    """Проверяем запрос добавления питомца с корректными данными, без фото"""

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_simple_pet(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name

def test_add_simple_pet_with_invalid_data(name='', animal_type='Овчарка',
                                     age='2'):
    """Проверяем запрос добавления питомца с некорректными данными или пустыми(пустое имя по логике не должно приниматься), без фото.
    Возвращает статус 400"""

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_simple_pet(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400
    assert result['name'] == name

def test_add_simple_pet_with_invalid_key_valid_data(name='Жучка', animal_type='Овчарка',
                                              age='2'):
    """Проверяем запрос добавления питомца с некорректными auth_key и возвращает статус 403"""

    # Задаем невалидный auth_key
    auth_key = invalid_auth_key

    # Добавляем питомца
    status, result = pf.add_simple_pet(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом

    assert status == 403
    # assert result['name'] != name

def test_successful_update_pet_photo_with_valid_data(pet_photo='images\cat1.jpg'):
    """Проверяем запрос добавления питомца с корректными данными"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Если список не пустой, то пробуем обновить его фото

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_photo(auth_key, my_pets['pets'][0]['id'], pet_photo)

        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['pet_photo'] == my_pets['pets'][0]['pet_photo']
    else:
        # если список питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("Список питомцев пустой")

def test_update_pet_photo_with_invalid_auth_key(pet_photo='images\cat1.jpg'):
    """Проверяем запрос добавления фото имеющегося питомца, некорректным auth_key и возвращает статус 403"""

    # Задаем невалидный ключ invalid_auth_key, пытаемся получить список своих питомцев и обновить фото
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Если запрос прошел и список не пустой, то пробуем обновить его фото с невалидным auth_key

    if len(my_pets['pets'])  > 0:
        status, result = pf.update_pet_photo(invalid_auth_key, my_pets['pets'][0]['id'], pet_photo)

        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

        # Проверяем что статус ответа = 403
        assert status == 403
        # assert result['pet_photo'] != my_pets['pets'][0]['pet_photo']
    else:
        # если список питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("Список питомцев пустой")

def test_add_new_pet_with_valid_data(name='Барбоскин', animal_type='двортерьер',
                                     age='4', pet_photo='images\dog1.jpg'):
    """Проверяем запрос добавления питомца с фото с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    # pet_photo = '''F:\Learn_PycharmProjects\pythonProject_24\tests\images\dog1.jpg'''

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name

def test_add_new_pet_with_invalid_data(name='', animal_type='Дворняга',
                                     age='8', pet_photo = 'images\dog1.jpg'):
    """Проверяем запрос добавления питомца с фото с некорректными данными(питомец с пустым именем не должен добавляться).
    Возврат статус 400"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    # pet_photo = '''F:\Learn_PycharmProjects\pythonProject_24\tests\images\dog1.jpg'''

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем статус 400
    assert status == 400


def test_add_new_pet_invalid_data_without_peth_photo(name='Дружок без фото', animal_type='Дворняга',
                                     age='8', pet_photo = ''):
    """Проверяем добавление питомца без фото в методе с обязательным фото.
    Возврат статус 400"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    # pet_photo = '''F:\Learn_PycharmProjects\pythonProject_24\tests\images\dog1.jpg'''

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400


def test_add_new_pet_invalid_data_with_txt_peth_photo(name='Дружок c TXT фото', animal_type='Дворняга',
                                     age='8', pet_photo = 'images\lol.txt'):
    """Проверяем добавление питомца с ТХТ файлом вместо jpg фото.
    Возврат статус 400"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    # pet_photo = '''F:\Learn_PycharmProjects\pythonProject_24\tests\images\dog1.jpg'''

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400


def test_add_new_pet_invalid_data_long_name_pet(name='Дружок с именем очень длииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииииинным', animal_type='Дворняга',
                                     age='8', pet_photo = 'images\dog1.jpg'):
    """Проверяем добавление питомца с длинным именем"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    # pet_photo = '''F:\Learn_PycharmProjects\pythonProject_24\tests\images\dog1.jpg'''

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    result['name'] == name

def test_add_new_pet_invalid_data_str_age(name='Дружок семи лет', animal_type='Дворняга',
                                     age='семь', pet_photo = 'images\lol.txt'):
    """Проверяем добавление питомца с некорректными данными(питомец с пустым именем).
    Возврат статуса 400"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    # pet_photo = '''F:\Learn_PycharmProjects\pythonProject_24\tests\images\dog1.jpg'''

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400


def test_add_new_pet_with_invalid_auth_key_valid_data(name='Джульбарс', animal_type='Дворняга',
                                     age='8', pet_photo = 'images\dog1.jpg'):

    """Проверяем Добавление питомца с невалидным Auth_key, но корректными данными.
    Возврат статуса 403."""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    # pet_photo = '''F:\Learn_PycharmProjects\pythonProject_24\tests\images\dog1.jpg'''

    # Ключ invalid_auth_key сохраняем в переменную auth_key
    auth_key = invalid_auth_key

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 403


def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images\cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()

def test_delete_self_pet_with_invalid_auth_key():
    """Проверяем возможность удаления питомца с невалидным auth_key"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images\cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление с невалидным auth_key
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(invalid_auth_key, pet_id)

    # print(status)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 403
    assert status == 403
    # assert pet_id in my_pets.values()

def test_successful_update_self_pet_info(name='Мурзик', animal_type='Котэ', age=5):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если список питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("Нет питомцев, некого обновлять")

def test_update_self_pet_info_invalid_str_age(name='Мурзик шести лет', animal_type='Котэ', age='шесть'):
    """Проверяем возможность обновления информации о питомце с указанием возраста текстом (можно только число)"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 400 и имя питомца не содержится в ответе запроса
        assert status == 400
        assert result['name'] != name
    else:
        # если список питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("Нет питомцев, некого обновлять")