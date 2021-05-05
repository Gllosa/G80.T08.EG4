"""Module """
import re
import json
from datetime import datetime

from secure_all.exception.access_management_exception import AccessManagementException
from secure_all.data.access_key import AccessKey
from secure_all.data.access_request import AccessRequest
from secure_all.cfg.access_manager_config import JSON_FILES_PATH
from .data.attribute_dni import Dni
from .data.attribute_access_code import AccessCode
from .data.attribute_key_labels import KeyLabels


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
    def find_credentials(dni):
        """ return the access request related to a given dni"""
        requests_store = JSON_FILES_PATH + "storeRequest.json"
        try:
            with open(requests_store, "r", encoding="utf-8", newline="") as file:
                list_data = json.load(file)
        except FileNotFoundError as ex:
            raise AccessManagementException("Wrong file or file path") from ex
        except json.JSONDecodeError as ex:
            raise AccessManagementException("JSON Decode Error - Wrong JSON Format") from ex
        for request in list_data: 
            if request["_AccessRequest__id_document"] == dni:
                return request
        return None

    @staticmethod
    def request_access_code(id_card, name_surname, access_type, email_address, days):
        """ this method give access to the building"""

        my_request = AccessRequest(id_card, name_surname, access_type, email_address, days)
        my_request.store_request()
        return my_request.access_code

    def get_access_key(self, key_file):
        my_key = AccessKey(key_file)
        # store the key generated.
        my_key.store_keys()
        return my_key.key

    def validate_access_code_for_dni(self, request_code, dni):
        # Comrpobar que el dni es correcto
        Dni(dni)
        # check if this dni is stored, and return in credentials all the info
        credentials = self.find_credentials(dni)
        if credentials is None:
            raise AccessManagementException("DNI is not found in the store")
        # generate the access code to check if it is correct
        access_request = AccessRequest(credentials['_AccessRequest__id_document'],
                                       credentials['_AccessRequest__name'],
                                       credentials['_AccessRequest__visitor_type'],
                                       credentials['_AccessRequest__email_address'],
                                       credentials['_AccessRequest__validity'])
        access_code = access_request.access_code
        if access_code != request_code:
            raise AccessManagementException("access code is not correct for this DNI")
        return credentials

    def open_door(self, key):
        # check if key is complain with the  correct format
        regex = r'[0-9a-f]{64}'
        if not re.fullmatch(regex, key):
            raise AccessManagementException("key invalid")
        keys_store = JSON_FILES_PATH + "storeKeys.json"
        keys_from_store = self.read_key_file(keys_store)
        justnow = datetime.utcnow()
        justnow_timestamp = datetime.timestamp(justnow)
        for key_in_store in keys_from_store:
            if key_in_store["_AccessKey__key"] == key \
                    and (key_in_store["_AccessKey__expiration_date"] > justnow_timestamp
                         or key_in_store["_AccessKey__expiration_date"] == 0):
                return True
        raise AccessManagementException("key is not found or is expired")
