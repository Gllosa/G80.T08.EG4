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


    @staticmethod
    def validate_dni( d ):
        """RETURN TRUE IF THE DNI IS RIGHT, OR FALSE IN OTHER CASE"""
        c = {"0": "T", "1": "R", "2": "W", "3": "A", "4": "G", "5": "M",
             "6": "Y", "7": "F", "8": "P", "9": "D", "10": "X", "11": "B",
             "12": "N", "13": "J", "14": "Z", "15": "S", "16": "Q", "17": "V",
             "18": "H", "19": "L", "20": "C", "21": "K", "22": "E"}
        v = int(d[ 0:8 ])
        r = str(v % 23)
        return d[8] == c[r]


    @staticmethod
    def check_dni( d ):
        """validating the dni syntax"""
        r = r'^[0-9]{8}[A-Z]{1}$'
        if re.fullmatch(r, d):
            return True
        raise AccessManagementException("DNI is not valid")

    @staticmethod
    def val( d, t ):
        """validating the validity days"""
        if not isinstance(d, int):
            raise AccessManagementException("days invalid")
        if (t == "Resident" and d == 0) or (t == "Guest" and d >= 2 and d <= 15):
            return True
        raise AccessManagementException("days invalid")

    @staticmethod
    def check_ac( a ):
        """Validating the access code syntax"""
        regex = '[0-9a-f]{32}'
        if re.fullmatch(regex, a):
            return True
        raise AccessManagementException("access code invalid")

    @staticmethod
    def check_labs( k ):
        """checking the labels of the input json file"""
        try:
            k[ "AccessCode" ]
            k[ "DNI" ]
            k[ "NotificationMail" ]
        except KeyError as ex:
            raise AccessManagementException("JSON Decode Error - Wrong label") from ex
        return True

    @staticmethod
    def read_key_file( f ):
        """read the list of stored elements"""
        try:
            with open(f, "r", encoding="utf-8", newline="") as file:
                data = json.load(file)
        except FileNotFoundError as ex:
            raise AccessManagementException("Wrong file or file path") from ex
        except json.JSONDecodeError as ex:
            raise AccessManagementException("JSON Decode Error - Wrong JSON Format") from ex
        return data

    @staticmethod
    def find_credentials( c ):
        """ return the access request related to a given dni"""
        f = JSON_FILES_PATH + "storeRequest.json"
        try:
            with open(f, "r", encoding="utf-8", newline="") as file:
                list_data = json.load(file)
        except FileNotFoundError as ex:
            raise AccessManagementException("Wrong file or file path") from ex
        except json.JSONDecodeError as ex:
            raise AccessManagementException("JSON Decode Error - Wrong JSON Format") from ex
        for k in list_data:
            if k["_AccessRequest__id_document"] == c:
                return k
        return None

    def request_access_code (self, id_card, name_surname, access_type, email_address, days):
        """ this method give access to the building"""

        r = r'^[a-z0-9]+[\._]?[a-z0-9]+[@](\w+[.])+\w{2,3}$'
        if not re.fullmatch(r, email_address):
            raise AccessManagementException("Email invalid")

        self.check_dni(id_card)
        r = r'(Resident|Guest)'
        if not re.fullmatch(r, access_type):
            raise AccessManagementException("type of visitor invalid")
        self.val(days, access_type)

        r = r'^[A-Za-z0-9]+(\s[A-Za-z0-9]+)+'
        if not re.fullmatch(r, name_surname):
            raise AccessManagementException("Invalid full name")

        if self.validate_dni(id_card):
            my_request = AccessRequest(id_card, name_surname, access_type, email_address, days)
            my_request.add_credentials()
            return my_request.access_code
        else:
            raise AccessManagementException("DNI is not valid")

    def get_access_key(self, keyfile):
        req = self.read_key_file(keyfile)
        #check if all labels are correct
        self.check_labs(req)
        # check if the values are correct
        self.check_dni(req["DNI"])
        self.check_ac(req[ "AccessCode" ])
        num_emails = 0
        for m in req["NotificationMail"]:
            num_emails = num_emails + 1
            r = r'^[a-z0-9]+[\._]?[a-z0-9]+[@](\w+[.])+\w{2,3}$'
            if not re.fullmatch(r, m):
                raise AccessManagementException("Email invalid")
        if num_emails < 1 or num_emails > 5:
            raise AccessManagementException("JSON Decode Error - Email list invalid")
        if not self.validate_dni(req["DNI"]):
            raise AccessManagementException("DNI is not valid")
        # check if this dni is stored, and return in k all the info
        k = self.find_credentials(req["DNI"])
        if k is None:
            raise AccessManagementException("DNI is not found in the store")

        # generate the acces code to check if it is correct
        n = AccessRequest(k['_AccessRequest__id_document'],
                          k['_AccessRequest__name'],
                          k['_AccessRequest__visitor_type'],
                          k['_AccessRequest__email_address'],
                          k['_AccessRequest__validity'])
        ac = n.access_code
        if ac != req["AccessCode"]:
            raise AccessManagementException("access code is not correct for this DNI")
        # if everything is ok , generate the key
        my_key= AccessKey(req["DNI"], req["AccessCode"],
                                     req["NotificationMail"],k["_AccessRequest__validity"])
        # store the key generated.
        my_key.store_keys()
        return my_key.key

    def open_door(self, key):
        #check if key is complain with the  correct format
        r = r'[0-9a-f]{64}'
        if not re.fullmatch(r, key):
            raise AccessManagementException("key invalid")
        f = JSON_FILES_PATH + "storeKeys.json"
        l = self.read_key_file(f)
        justnow = datetime.utcnow()
        justnow_timestamp = datetime.timestamp(justnow)
        for k in l :
            if k["_AccessKey__key"] == key \
                    and (k["_AccessKey__expiration_date"] > justnow_timestamp
                         or k["_AccessKey__expiration_date"] == 0):
                return True
        raise AccessManagementException("key is not found or is expired")
