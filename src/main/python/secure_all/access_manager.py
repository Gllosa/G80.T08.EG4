"""Module """
import re
import json
from datetime import datetime

from .access_management_exception import AccessManagementException
from .access_key import AccessKey
from .access_request import AccessRequest
from .access_manager_config import JSON_FILES_PATH


class AccessManager:
    """Class for providing the methods for managing the access to a building"""

    def __init__(self):
        pass

    def validate_dni(self, dni):
        """RETURN TRUE IF THE DNI IS RIGHT, OR FALSE IN OTHER CASE"""
        self.validate_dni_syntax(dni)
        return self.validate_dni_character(dni)

    @staticmethod
    def validate_dni_character(dni):
        letra_control = {"0": "T", "1": "R", "2": "W", "3": "A", "4": "G", "5": "M",
                         "6": "Y", "7": "F", "8": "P", "9": "D", "10": "X", "11": "B",
                         "12": "N", "13": "J", "14": "Z", "15": "S", "16": "Q", "17": "V",
                         "18": "H", "19": "L", "20": "C", "21": "K", "22": "E"}
        numero_dni = int(dni[0:8])
        clave_letra = str(numero_dni % 23)
        return dni[8] == letra_control[clave_letra]

    @staticmethod
    def validate_dni_syntax(dni):
        """validating the dni syntax"""
        expresion_regex = r'^[0-9]{8}[A-Z]{1}$'
        if re.fullmatch(expresion_regex, dni):
            return True
        raise AccessManagementException("DNI is not valid")

    @staticmethod
    def validate_days(days, guest_type):
        """validating the validity days"""
        if not isinstance(days, int):
            raise AccessManagementException("days invalid")
        if (guest_type == "Resident" and days == 0) or (guest_type == "Guest" and 2 <= days <= 15):
            return True
        raise AccessManagementException("days invalid")

    @staticmethod
    def check_access_code(access_code):
        """Validating the access code syntax"""
        regex = '[0-9a-f]{32}'
        if re.fullmatch(regex, access_code):
            return True
        raise AccessManagementException("access code invalid")

    @staticmethod
    def check_labels(json_dict):
        """checking the labels of the input json file"""
        try:
            json_dict["AccessCode"]
            json_dict["DNI"]
            json_dict["NotificationMail"]
        except KeyError as ex:
            raise AccessManagementException("JSON Decode Error - Wrong label") from ex
        return True

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

    def request_access_code(self, id_card, name_surname, access_type, email_address, days):
        """ this method give access to the building"""

        self.validate_email(email_address)

        regex = r'(Resident|Guest)'
        if not re.fullmatch(regex, access_type):
            raise AccessManagementException("type of visitor invalid")
        self.validate_days(days, access_type)

        regex = r'^[A-Za-z0-9]+(\s[A-Za-z0-9]+)+'
        if not re.fullmatch(regex, name_surname):
            raise AccessManagementException("Invalid full name")

        if self.validate_dni(id_card):
            my_request = AccessRequest(id_card, name_surname, access_type, email_address, days)
            my_request.add_credentials()
            return my_request.access_code
        else:
            raise AccessManagementException("DNI is not valid")

    @staticmethod
    def validate_email(email_address):
        email_pattern = r'^[a-z0-9]+[\._]?[a-z0-9]+[@](\w+[.])+\w{2,3}$'
        if not re.fullmatch(email_pattern, email_address):
            raise AccessManagementException("Email invalid")

    def get_access_key(self, key_file):
        request = self.read_key_file(key_file)
        # check if all labels are correct
        self.check_labels(request)
        # check if the values are correct
        self.validate_dni_syntax(request["DNI"])
        self.check_access_code(request["AccessCode"])
        num_emails = 0
        for email in request["NotificationMail"]:
            num_emails = num_emails + 1
            r = r'^[a-z0-9]+[\._]?[a-z0-9]+[@](\w+[.])+\w{2,3}$'
            if not re.fullmatch(r, email):
                raise AccessManagementException("Email invalid")
        if num_emails < 1 or num_emails > 5:
            raise AccessManagementException("JSON Decode Error - Email list invalid")
        if not self.validate_dni(request["DNI"]):
            raise AccessManagementException("DNI is not valid")
        # check if this dni is stored, and return in credentials all the info
        credentials = self.find_credentials(request["DNI"])
        if credentials is None:
            raise AccessManagementException("DNI is not found in the store")

        # generate the access code to check if it is correct
        access_request = AccessRequest(credentials['_AccessRequest__id_document'],
                                       credentials['_AccessRequest__name'],
                                       credentials['_AccessRequest__visitor_type'],
                                       credentials['_AccessRequest__email_address'],
                                       credentials['_AccessRequest__validity'])
        access_code = access_request.access_code
        if access_code != request["AccessCode"]:
            raise AccessManagementException("access code is not correct for this DNI")
        # if everything is ok , generate the key
        my_key = AccessKey(request["DNI"], request["AccessCode"],
                           request["NotificationMail"], credentials["_AccessRequest__validity"])
        # store the key generated.
        my_key.store_keys()
        return my_key.key

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
