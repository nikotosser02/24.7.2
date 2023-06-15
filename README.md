# 24.7.2


В директории /tests располагается файл с тестами

В директории /tests/images лежат картинки для теста добавления питомца и теста добавления картинки

В корневой директории лежит файл settings.py - содержит информацию о валидном логине и пароле

В корневой директории лежит файл api.py, который является библиотекой к REST api сервису веб приложения Pet Friends

Библиотека api написана в классе, что соответствует принципам ООП и позволяет удобно пользоваться её методами.
При инициализации библиотеки объявляется переменная base_url которая используется при формировании url для запроса.

Методы имеют подродное описание.

Тесты проверяют работу методов используя api библиотеку.


----------------------------------------------------------------------

К методам курса добавлены тесты/методы

test_get_api_key_for_invalid_user
Получение ключа с невалидными логин/пасс

test_get_all_pets_with_invalid_user
Получение списка питомцев с невалидными логин/пасс

test_get_all_pets_with_invalid_key
Получение списка питомцев с невалидным auth_key

test_add_simple_pet_with_valid_data
Запрос добавления питомца без фото

test_add_simple_pet_with_invalid_data
Запрос добавления питомца без фото с невалидными данными

test_add_simple_pet_with_invalid_key_valid_data
Запрос добавления питомца без фото с невалидными auth_key но валидными данными

test_add_new_pet_with_invalid_data
Запрос добавления питомца с фото и невалидными данными

test_add_new_pet_with_invalid_auth_key_valid_data
Запрос добавления питомца с фото и валидными данными, но невалидным auth_key

test_add_new_pet_invalid_data_without_peth_photo
Запрос добавления питомца с отсутстыующим фото и невалидными данными

test_add_new_pet_invalid_data_with_txt_peth_photo
Запрос добавления питомца с фото, невалидными данными(ТХТ файл вместо фото)

test_add_new_pet_invalid_data_long_name_pet
Запрос добавления питомца с фото и очень длинным именем

test_add_new_pet_invalid_data_str_age
Запрос добавления питомца с фото и возрастом переданным текстом, а не числом

test_update_self_pet_info_invalid_str_age
Запрос на изменение данных о питомце с указанием возраста текстом, а не числом

test_successful_update_pet_photo_with_valid_data
Запрос на добавление фото существующего питомца и валидными данными

test_update_pet_photo_with_invalid_auth_key
Запрос на добавление фото существующего питомца и невалидным auth_key

test_delete_self_pet_with_invalid_auth_key
Запрос на удаление питомца с невалидным auth_key
