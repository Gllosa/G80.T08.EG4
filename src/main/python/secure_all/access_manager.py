"""Module """
import re
import json
from datetime import datetime

from secure_all.exception.access_management_exception import AccessManagementException
from secure_all.data.access_key import AccessKey
from secure_all.data.access_request import AccessRequest
from secure_all.cfg.access_manager_config import JSON_FILES_PATH
from secure_all.data.attribute_key import Key
from secure_all.storage.keys_json_store import KeysJsonStore


class AccessManager:
    """Class for providing the methods for managing the access to a building"""

    def __init__(self):
        pass

    @staticmethod
    def read_key_file(file):
        """read the list of stored elements"""
        try:
            with open(file, "r", encoding="utf-8", newline="") as file:
                data = json.load(file)
        except FileNotFoundError as ex:
            raise AccessManagementException("Wrong file or file path") from ex
        except json.JSONDecodeError as ex:
            raise AccessManagementException("JSON Decode Error - Wrong JSON Format") from ex
        print(data)
        return data

    @staticmethod
    def request_access_code(id_card, name_surname, access_type, email_address, days):
        """ this method give access to the building"""

        my_request = AccessRequest(id_card, name_surname, access_type, email_address, days)
        my_request.store_request()
        return my_request.access_code

    @staticmethod
    def get_access_key(key_file):
        my_key = AccessKey(key_file)
        # store the key generated.
        my_key.store_keys()
        return my_key.key

    @staticmethod
    def open_door(key):
        Key(key)
        keys_store = KeysJsonStore()
        return keys_store.is_valid(key)
