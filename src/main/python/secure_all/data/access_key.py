"""Contains the class Access Key"""
from datetime import datetime
import hashlib
import json

from secure_all.cfg.access_manager_config import JSON_FILES_PATH
from secure_all.exception.access_management_exception import AccessManagementException
from secure_all.data.attribute_access_code import AccessCode
from secure_all.data.attribute_dni import Dni
from secure_all.data.attribute_notification_emails import NotificationEmails
from secure_all.storage.keys_json_store import KeysJsonStore
from secure_all import AccessRequest
from secure_all.parser.key_json_parser import KeyJsonParser


class AccessKey:
    """Class representing the key for accessing the building"""
    ERROR_DNI_NOT_FOUND = "DNI is not found in the store"
    ERROR_ACCESS_CODE_WRONG = "access code is not correct for this DNI"
    ERROR_WRONG_FILE = "Wrong file or file path"
    JSON_DECODE_ERROR = "JSON Decode Error - Wrong JSON Format"

    def __init__(self, key_file):

        request = KeyJsonParser(key_file).json_content
        # check if all labels are correct
        # Comprobar que el codigo de acceso es valido
        credentials = self.validate_access_code_for_dni(AccessCode(request["AccessCode"]).value,
                                                        request["DNI"])

        self.__alg = "SHA-256"
        self.__type = "DS"
        self.__dni = Dni(request["DNI"]).value
        self.__access_code = AccessCode(request["AccessCode"]).value
        self.__notification_emails = NotificationEmails(request["NotificationMail"]).value
        justnow = datetime.utcnow()
        self.__issued_at = datetime.timestamp(justnow)
        # fix self.__issued_at only for testing 13-3-2021 18_49
        self.__issued_at = 1615627129.580297
        if credentials["_AccessRequest__validity"] == 0:
            self.__expiration_date = 0
        else:
            # timestamp is represneted in seconds.microseconds
            # validity must be expressed in senconds to be added to the timestap
            tiempo_validez = credentials["_AccessRequest__validity"] * 30 * 24 * 60 * 60
            self.__expiration_date = self.__issued_at + tiempo_validez
        self.__key = hashlib.sha256(self.__signature_string().encode()).hexdigest()

    def __signature_string(self):
        """Composes the string to be used for generating the key"""
        return "{alg:" + self.__alg + ",typ:" + self.__type + ",accesscode:" \
               + self.__access_code + ",issuedate:" + str(self.__issued_at) \
               + ",expirationdate:" + str(self.__expiration_date) + "}"

    def validate_access_code_for_dni(self, request_code, dni):
        """Valida un codiog de acceso para un determinado dni"""
        # Comprobar que el dni es correcto
        # check if this dni is stored, and return in credentials all the info
        credentials = self.find_credentials(Dni(dni).value)
        if credentials is None:
            raise AccessManagementException(self.ERROR_DNI_NOT_FOUND)
        # generate the access code to check if it is correct
        access_request = AccessRequest(credentials['_AccessRequest__id_document'],
                                       credentials['_AccessRequest__name'],
                                       credentials['_AccessRequest__visitor_type'],
                                       credentials['_AccessRequest__email_address'],
                                       credentials['_AccessRequest__validity'])
        access_code = access_request.access_code
        if access_code != request_code:
            raise AccessManagementException(self.ERROR_ACCESS_CODE_WRONG)
        return credentials

    def find_credentials(self, dni):
        """ return the access request related to a given dni"""
        requests_store = JSON_FILES_PATH + "storeRequest.json"
        try:
            with open(requests_store, "r", encoding="utf-8", newline="") as file:
                list_data = json.load(file)
        except FileNotFoundError as ex:
            raise AccessManagementException(self.ERROR_WRONG_FILE) from ex
        except json.JSONDecodeError as ex:
            raise AccessManagementException(self.JSON_DECODE_ERROR) from ex
        for request in list_data:
            if request["_AccessRequest__id_document"] == dni:
                return request
        return None

    def store_keys(self):
        """ srote de keys """
        key_store = KeysJsonStore()
        key_store.add_item(self)
        key_store.save_store()

    @property
    def expiration_date(self):
        """expiration_date getter"""
        return self.__expiration_date

    @expiration_date.setter
    def expiration_date(self, value):
        """expiration_date setter"""
        self.__expiration_date = value

    @property
    def dni(self):
        """Property that represents the dni of the visitor"""
        return self.dni

    @dni.setter
    def dni(self, value):
        """dni setter"""
        self.__dni = value

    @property
    def access_code(self):
        """Property that represents the access_code of the visitor"""
        return self.__access_code

    @access_code.setter
    def access_code(self, value):
        """access_code setter"""
        self.__access_code = value

    @property
    def notification_emails(self):
        """Property that represents the access_code of the visitor"""
        return self.__notification_emails

    @notification_emails.setter
    def notification_emails(self, value):
        self.__notification_emails = value

    @property
    def key(self):
        """Getter de key"""
        return self.__key

    @key.setter
    def key(self, value):
        self.__key = value

    #    @property
    #    def key(self):
    #        """Returns the sha256 signature"""
    #        return hashlib.sha256(self.__signature_string().encode()).hexdigest()
