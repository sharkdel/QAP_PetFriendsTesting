from api import PetFriends
from settings import valid_email, valid_password, no_valid_password, no_valid_email
import os

pf = PetFriends()


def test_get_api_for_no_valid_email(email=no_valid_email, password=valid_password):
    """ Вводим неверный логин и проверяем что запрос api ключа возвращает статус 403 и
    в результате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403
    assert 'key' in result


def test_get_api_for_no_valid_password(email=valid_email, password=no_valid_password):
    """ Вводим неверный пароль и проверяем что запрос api ключа возвращает статус 403 и
    в результате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403
    assert 'key' in result


def test_get_all_pets_with_no_valid_mail(filter=''):
    """ Проверяем что запрос всех питомцев не возвращает список питомцев при указании неверного email """

    _, auth_key = pf.get_api_key(no_valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 403
    assert len(result['pets']) > 0


def test_get_all_pets_with_no_valid_key(filter=''):
    """ Проверяем что запрос всех питомцев не возвращает список питомцев при указании неверного пароля """

    _, auth_key = pf.get_api_key(valid_email, no_valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 403
    assert len(result['pets']) > 0


def test_add_new_pet_with_no_valid_data(name='', animal_type='', age=3, pet_photo='images/cat1.txt'):
    """Проверяем, что можно добавить питомца с пустыми полями"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.post_add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400
    assert result['name'] == name


def test_add_new_pet_with_no_valid_photo(name='Pet', animal_type='photo', age=3, pet_photo='images/cat1.txt'):
    """Проверяем, что можно добавить питомца с некорректными данными, а именно с текстовым файлом вместо фото"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.post_add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400
    assert result['name'] == name


def test_add_photo_of_pet_no_valid_photo(pet_photo='images/cat1.txt'):
    """Проверяем, что можно добавить к существующему питомцу вместо фото текстовый файл."""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key, запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.post_add_new_pet(auth_key, "Суперкот", "кот", 3, "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берем id последнего добавленного питомца
    pet_id = my_pets['pets'][0]['id']
    status, result = pf.post_add_photo_of_pet(auth_key, pet_id, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400
    assert result['pet_photo'] != ''


def test_add_new_pet_without_data(name='', animal_type='', age=''):
    """Проверяем что можно добавить питомца с пустыми данными и без загрузки его фото"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.post_add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400
    assert result['name'] == name
    print()
    print(status)


def test_unsuccessful_delete_self_pet():
    """Проверяем возможность удаления питомца c неверным ключом"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = 200, '46765878679'
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.post_add_new_pet(auth_key, "Суперкот", "кот", 3, "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 403
    assert pet_id not in my_pets.values()


def test_unsuccessful_update_self_pet_info(name='Мурзннннннннннннннннннннннннннннрррррррр',
                                           animal_type='Некто', age=555):
    """Проверяем возможность обновления информации о питомце c некорректными данными"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.put_update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 400
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")