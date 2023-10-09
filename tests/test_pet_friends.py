import os

from api import PetFriends
from setting import valid_email, valid_password, invalid_email, invalid_password


pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):

    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашим ожиданием
    assert status == 200
    assert 'key' in result

def test_get_api_for_invalid_user(email=invalid_email,password=invalid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200

def test_get_all_pets_with_valid_key(filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(filter)

    assert status == 200
    assert len(result['pets']) > 0

def test_unseccessful_get_all_pets_with_invalid_key(filter=''):
    _, auth_key = pf.get_api_key(invalid_email, invalid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0

def test_successful_update_self_pet_info(name='БарSik',
                                         animal_type='', age=5):
   _, auth_key = pf.get_api_key(valid_email, valid_password)
   _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

   if len(my_pets['pets']) > 0:
       status, result = pf.update_info_about_pet(auth_key, my_pets['pets'][0]['id'],
                                                name, animal_type, age)
       assert status == 200
       assert result['name'] == name
   else:
       raise Exception("There is no my pets")

def test_successful_add_photo_of_pet(pet_photo='images/cat1.jpg'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        pet_id = my_pets['pets'][0]['id']
        status, result = pf.add_photo_of_pet(auth_key, pet_id, pet_photo)

        assert status == 200
        assert result['pet_photo'] == pet_photo
    else:
        raise Exception("There is no my pets")

def test_successful_delete_self_pet():
       _, auth_key = pf.get_api_key(valid_email, valid_password)
       _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

       if len(my_pets['pets']) == 0:
           pf.add_new_pet(auth_key, "Barsik", "cat", "2", "images/cat1.jpg")
           _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

       pet_id = my_pets['pets'][0]['id']
       status, result = pf.delete_pet(auth_key, pet_id)

       _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

       assert status == 200
       assert pet_id not in my_pets.values()

