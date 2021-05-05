"""MODULE: access_request. Contains the access request class"""
import json
import hashlib
from secure_all.cfg.access_manager_config import JSON_FILES_PATH
from secure_all.exception.access_management_exception import AccessManagementException
from secure_all.data.attribute_full_name import FullName
from secure_all.data.attribute_email import Email
from secure_all.data.attribute_visitor_type import VisitorType
from secure_all.data.attribute_validity import Validity
from secure_all.data.attribute_dni import Dni
from secure_all.storage.requests_json_store import RequestJsonStore


class AccessRequest:
    """Class representing the access request"""

    def __init__(self, id_document, full_name, visitor_type, email_address, validity):
        self.__id_document = Dni(id_document).value
        self.__name = FullName(full_name).value
        self.__visitor_type = VisitorType(visitor_type).value
        self.__email_address = Email(email_address).value
        self.__validity = Validity(validity, visitor_type).value
        # justnow = datetime.utcnow()
        # self.__time_stamp = datetime.timestamp(justnow)
        # only for testing , fix de time stamp to this value 1614962381.90867 , 5/3/2020 18_40
        self.__time_stamp = 1614962381.90867

    def __str__(self):
        return "AccessRequest:" + json.dumps(self.__dict__)

    @property
    def name(self):
        """Property representing the name and the surname of
        the person who request access to the building"""
        return self.__name

    @name.setter
    def name(self, value):
        """name setter"""
        self.__name = value

    @property
    def visitor_type(self):
        """Property representing the type of visitor: Resident or Guest"""
        return self.__visitor_type

    @visitor_type.setter
    def visitor_type(self, value):
        self.__visitor_type = value

    @property
    def email_address(self):
        """Property representing the requester's email address"""
        return self.__email_address

    @email_address.setter
    def email_address(self, value):
        self.__email_address = value

    @property
    def id_document(self):
        """Property representing the requester's DNI"""
        return self.__id_document

    @id_document.setter
    def id_document(self, value):
        self.__id_document = value

    @property
    def time_stamp(self):
        """Read-only property that returns the timestamp of the request"""
        return self.__time_stamp

    @property
    def access_code(self):
        """Property for obtaining the access code according the requirements"""
        return hashlib.md5(self.__str__().encode()).hexdigest()

    def store_request(self):
        request_store = RequestJsonStore()
        request_store.add_item(self)
        del request_store
