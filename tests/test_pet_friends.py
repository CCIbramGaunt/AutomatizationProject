import pytest
import requests
from api import PetActions, base_URL
from settings import valid_email, valid_password

testname = 'Jimmy'
testtype = 'dog'
testage = 1
photo_URL = '../tests/images/chibis.jpg'

class TestActions:
    def setup(self):
        """Начало тестирования"""
        self.act = PetActions

    def test_getting_api(self):
        """Попытка получить API-ключ с сервера, предоставив правильные email и пароль"""
        assert self.act.get_api_key(valid_email, valid_password)[1] == 200

    def test_getting_api_wrong_credentials(self):
        """Попытка получить API-ключ с неправильной парой логин-пароль"""
        assert self.act.get_api_key('valid_email', 'valid_password') == 403

    def test_posting_new_pet_correct(self):
        """Попытка разместить инфо по питомцу с правильными параметрами"""
        assert self.act.post_new_pet(testname, testtype, testage, photo_URL)[1] == 200

    def test_posting_new_pet_incorrect(self):
        """Попытка разместить инфо по питомцу с неправильным именем"""
        assert self.act.post_new_pet(testage, testtype, testage, photo_URL)[1] == 400

    def test_creating_pet_simple(self):
        """Попытка разместить инфо по питомцу по упрощенной форме с правильными параметрами"""
        assert self.act.create_pet_simple(testname, testtype, testage)[1] == 200

    """Эти переменные потребуются для тестирования функций update и delete"""
    global pet_id
    pet_id = PetActions.post_new_pet(testname, testtype, testage, photo_URL)[0]
    global pet_id_no_photo
    pet_id_no_photo = PetActions.create_pet_simple(testname, testtype, testage)[0]

    def test_updating_pet(self):
        """Попытка изменить информацию по имеющемуся питомцу с корректными данными"""
        assert self.act.update_pet(f'{pet_id}', 'Bobby', 'cat', 12)[1] == 200

    def test_updating_pet_incorrect_name(self):
        """Попытка изменить информацию по имеющемуся питомцу с именем в числовом формате"""
        assert self.act.update_pet(f'{pet_id}', 123, 'cat', 12)[1] == 400

    def test_updating_pet_incorrect_age(self):
        """Попытка изменить информацию по имеющемуся питомцу с возрастом в формате строки"""
        assert self.act.update_pet(f'{pet_id}', 'Bobby', 'cat', 'twelve')[1] == 400

    def test_updating_nonexistent_pet(self):
        """Попытка изменить информацию по несуществующему питомцу с корректными данными"""
        assert self.act.update_pet(pet_id*2, 'Bobby', 'cat', 12)[1] == 400

    def test_deleting_pet(self):
        """Попытка удалить информацию по имеющемуся питомцу"""
        assert self.act.delete_pet(pet_id)[1] == 200

    def test_deleting_nonexistent_pet(self):
        """Попытка удалить информацию по несуществующему питомцу"""
        assert self.act.delete_pet(pet_id*2)[1] != 200

    def test_getting_my_pets(self):
        """Попытка получить список своих питомцев с правильным фильтром"""
        assert self.act.get_my_pets_list('my_pets')[1] == 200

    def test_getting_my_pets_wrong_filter(self):
        """Попытка получить список своих питомцев с правильным API и неправильным фильтром"""
        assert self.act.get_my_pets_list('111')[1] == 500

    def test_getting_all_pets(self):
        """Попытка получить список всех питомцев с правильным API"""
        assert self.act.get_all_pets_list()[1] == 200

    def test_adding_pet_photo(self):
        """Попытка добавить фото к анкете существующего питомца с корректными данными"""
        assert self.act.add_pet_photo(pet_id_no_photo, photo_URL)[1] == 200

    def test_adding_pet_photo_incorrect(self):
        """Попытка добавить фото к анкете существующего питомца с числом вместо ссылки на фото"""
        with pytest.raises(OSError):
            self.act.add_pet_photo(pet_id_no_photo, 123)

    def test_getting_all_pets_wrong_API(self):
        """Попытка получить список всех питомцев с неправильным API-ключом"""
        assert requests.get(f'{base_URL}/api/pets', headers={'auth_key': 'wrong API'}).status_code == 403

    def test_creating_pet_simple_wrong_API(self):
        """Попытка создать упрощенную карточку питомца с неправильным API-ключом"""
        new_pet = {
            'name': testname,
            'animal_type': testtype,
            'age': testage
        }
        assert requests.post(f'{base_URL}/api/create_pet_simple', \
                headers={'auth_key': 'wrong API'}, data=new_pet).status_code == 403

    def teardown(self):
        """Завершение тестирования"""
        print('Выполнение метода teardown')