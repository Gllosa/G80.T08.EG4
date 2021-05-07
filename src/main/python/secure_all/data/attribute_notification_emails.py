"""Module"""
import re

from secure_all.exception.access_management_exception import AccessManagementException
from .attribute import Attribute


class NotificationEmails(Attribute):
    """Clase para validar los emails"""
    EMAIL_ERROR = "Email invalid"
    JSON_DECODE_ERROR = "JSON Decode Error - Email list invalid"

    def __init__(self, attr_value):
        super().__init__(attr_value, '', "")
        self.attr_value = self._validate(attr_value)

    def _validate(self, attr_value):
        num_emails = 0
        for email in attr_value:
            num_emails = num_emails + 1
            regex_sintax = r'^[a-z0-9]+[\._]?[a-z0-9]+[@](\w+[.])+\w{2,3}$'
            if not re.fullmatch(regex_sintax, email):
                raise AccessManagementException(self.EMAIL_ERROR)
        if num_emails < 1 or num_emails > 5:
            raise AccessManagementException(self.JSON_DECODE_ERROR)
        return attr_value
