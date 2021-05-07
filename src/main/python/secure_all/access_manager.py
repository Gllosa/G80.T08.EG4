"""Module """
from secure_all.data.access_key import AccessKey
from secure_all.data.access_request import AccessRequest
from secure_all.storage.keys_json_store import KeysJsonStore


class AccessManager:
    """Class for providing the methods for managing the access to a building"""

    def __init__(self):
        pass

    @staticmethod
    def request_access_code(id_card, name_surname, access_type, email_address, days):
        """ this method give access to the building"""

        my_request = AccessRequest(id_card, name_surname, access_type, email_address, days)
        my_request.store_request()
        return my_request.access_code

    @staticmethod
    def get_access_key(key_file):
        """Devuelve la llave"""
        my_key = AccessKey(key_file)
        my_key.store_keys()
        return my_key.key

    @staticmethod
    def open_door(key):
        """Abre la puerta con una llave"""
        keys_store = KeysJsonStore()
        return keys_store.is_valid(key)
