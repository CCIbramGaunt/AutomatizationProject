import requests
import json
from settings import valid_email, valid_password

base_URL = 'https://petfriends.skillfactory.ru'


class PetActions:
    def get_api_key(email: str, password: str) -> str:
        """Метод отправляет запрос к API сервера, передавая email и пароль пользователя, а возвращает полученный
        API ключ в виде строки"""
        headers = {
            'accept': 'application/json',
            'email': email,
            'password': password
        }
        res = requests.get(f'{base_URL}/api/key', headers=headers)
        if res.status_code == 200:
            return res.json()['key'], res.status_code
        else:
            return res.status_code

    def post_new_pet(name: str, animal_type: str, age: float, pet_photo: str) -> json:
        """Метод отправляет на сервер запрос о размещении нового питомца со следующими параметрами: имя, тип, возраст,
         фото. Возвращает JSON (либо текстовый) ответ сервера с данными нового питомца"""
        headers = {
            'auth_key': API
        }
        new_pet = {
            'name': name,
            'animal_type': animal_type,
            'age': age
        }
        file = {'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')}
        res = requests.post(f'{base_URL}/api/pets', headers=headers, data=new_pet, files=file)
        if res.status_code == 200:
            print(f'{name} the {age} year old {animal_type} was added successfully')
        else:
            print(res.status_code)
        pet_id = res.json()['id']
        return pet_id, res.status_code, API

    def create_pet_simple(name: str, animal_type: str, age: float) -> json:
        """Метод отправляет на сервер запрос о размещении нового питомца со следующими параметрами: имя, тип, возраст.
         Возвращает JSON (либо текстовый) ответ сервера с данными нового питомца"""
        headers = {
            'auth_key': API
        }
        new_pet = {
            'name': name,
            'animal_type': animal_type,
            'age': age
        }
        res = requests.post(f'{base_URL}/api/create_pet_simple', headers=headers, data=new_pet)
        if res.status_code == 200:
            print(f'{name} the {age} year old {animal_type} was added successfully')
        else:
            print(res.status_code)
        pet_id_simple = res.json()['id']
        return pet_id_simple, res.status_code

    def update_pet(pet_id: str, name: str, animal_type: str, age: float) -> json:
        """Метод отправляет на сервер запрос об обновлении информации о питомце со следующими новыми параметрами:
        имя, тип, возраст. Возвращает JSON ответ сервера с данными нового питомца"""
        header = {'auth_key': API}
        updated_pet = {
            'name': name,
            'animal_type': animal_type,
            'age': age
        }
        res = requests.put(f'{base_URL}/api/pets/{pet_id}', headers=header, data=updated_pet)
        if res.status_code == 200:
            print(f'Информация по питомцу с id {pet_id} была обновлена')
        else:
            print(f'Обновление информации не выполнено, код ответа: ', res.status_code)
        return pet_id, res.status_code

    def add_pet_photo(pet_id: str, pet_photo: str) -> json:
        """Метод отправляет на сервер запрос о добавлении в информацию о питомце его фото.
         Возвращает JSON ответ сервера с данными нового питомца"""
        header = {'auth_key': API}
        file = {'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')}
        res = requests.post(f'{base_URL}/api/pets/set_photo/{pet_id}', headers=header, files=file)
        if res.status_code == 200:
            print(f'К информации о питомце с id {pet_id} было добавлено фото')
        else:
            print(f'Добавление фото не выполнено, код ответа: ', res.status_code)
        return pet_id, res.status_code

    def delete_pet(pet_id: str) -> json:
        """Метод отправляет на сервер запрос об удалении питомца с указанием его ID.
            Возвращает JSON (либо текстовый) ответ сервера с данными удаленного питомца"""
        header = {'auth_key': API}
        res = requests.delete(f'{base_URL}/api/pets/{pet_id}', headers=header)
        if res.status_code == 200:
            print(f'Питомец с id {pet_id} был удален')
        else:
            print(f'Удаление не выполнено, код ответа: ', res.status_code)
        return res, res.status_code

    def get_my_pets_list(filter: str) -> json:
        """Метод отправляет на сервер запрос на получение списка питомцев с фильтром "мои".
            Возвращает JSON-массив с данными питомцев, созданных с данным API"""
        header = {'auth_key': API}
        res = requests.get(f'{base_URL}/api/pets?filter={filter}', headers=header)
        if res.status_code == 200:
            print('Список Ваших питомцев получен')
        else:
            print(f'Список не получен, код ответа: ', res.status_code)
        return res, res.status_code

    def get_all_pets_list() -> json:
        """Метод отправляет на сервер запрос на получение списка питомцев с фильтром "мои".
            Возвращает JSON-массив с данными питомцев, созданных с данным API"""
        header = {'auth_key': API}
        res = requests.get(f'{base_URL}/api/pets', headers=header)
        if res.status_code == 200:
            print('Список всех питомцев получен')
        else:
            print(f'Список не получен, код ответа: ', res.status_code)
        return res, res.status_code

API =  PetActions.get_api_key(valid_email, valid_password)[0]

Bob = PetActions.post_new_pet('Bob', 'cat', 12, 'C:/Users/Supervisor/Desktop/Study/python/19.2.4/AutomatizationProject/tests/images/chibis.jpg')
print(Bob)


Stan = PetActions.create_pet_simple('Stan', 'fish', 2)
print(Stan)

print(PetActions.update_pet(f'{Bob[0]}', 'Bobby', 'cat', 12))

print(PetActions.add_pet_photo(Stan[0], 'C:/Users/Supervisor/Desktop/Study/python/19.2.4/AutomatizationProject/tests/images/GoogleImages.jpg'))

print(PetActions.delete_pet(f'{Bob[0]}'))

print(PetActions.get_my_pets_list('my_pets'))

print(PetActions.get_all_pets_list())


