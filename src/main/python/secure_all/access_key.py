"""Contains the class Access Key"""
from datetime import datetime
import hashlib
import json

from .access_manager_config import JSON_FILES_PATH
from .access_management_exception import AccessManagementException

class AccessKey():
    """Class representing the key for accessing the building"""

    def __init__(self, dni, access_code, notification_emails, validity):
        self.__alg = "SHA-256"
        self.__type = "DS"
        self.__dni = dni
        self.__access_code = access_code
        self.__notification_emails = notification_emails
        justnow = datetime.utcnow()
        self.__issued_at = datetime.timestamp(justnow)
        # fix self.__issued_at only for testing 13-3-2021 18_49
        self.__issued_at=1615627129.580297
        if validity == 0:
            self.__expiration_date = 0
        else:
            #timestamp is represneted in seconds.microseconds
            #validity must be expressed in senconds to be added to the timestap
            self.__expiration_date = self.__issued_at + (validity * 30 * 24 * 60 *60)
        self.__key = hashlib.sha256(self.__signature_string().encode()).hexdigest()

    def __signature_string(self):
        """Composes the string to be used for generating the key"""
        return "{alg:"+self.__alg + ",typ:" + self.__type + ",accesscode:"\
               + self.__access_code+",issuedate:"+str(self.__issued_at)\
               + ",expirationdate:" + str(self.__expiration_date) + "}"
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
    def dni(self,value):
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
    def notification_emails( self, value ):
        self.__notification_emails = value

    @property
    def key(self):
        return self.__key

    @key.setter
    def key(self, value):
        self.__key = value

    #    @property
#    def key(self):
#        """Returns the sha256 signature"""
#        return hashlib.sha256(self.__signature_string().encode()).hexdigest()


    def store_keys(self):
        """ srote de keys """
        myFile = JSON_FILES_PATH + "storeKeys.json"
        try:
            with open(myFile, "r",encoding="utf-8", newline="") as file:
                list_keys = json.load(file)
            # append the new key
            list_keys.append(self.__dict__)
            # write all the keys in the file
            with open(myFile, "w", encoding="utf-8", newline="") as file:
                json.dump(list_keys, file, indent=2)
        except FileNotFoundError as ex:
            # if file is not found, store the first key
            with open(myFile, "x", encoding="utf-8", newline="") as file:
                data_key = [self.__dict__]
                json.dump(data_key, file, indent=2)
        except json.JSONDecodeError as ex:
            raise AccessManagementException("JSON Decode Error - Wrong JSON Format") from ex
