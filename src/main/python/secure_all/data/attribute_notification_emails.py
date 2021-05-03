import re
from .attribute import Attribute
from secure_all.access_management_exception import AccessManagementException


class NotificationEmails(Attribute):
    def __init__(self, attr_value):
        super().__init__(attr_value, '', "")
        self.attr_value = self._validate(attr_value)

    def _validate(self, attr_value):
        num_emails = 0
        for email in attr_value:
            num_emails = num_emails + 1
            r = r'^[a-z0-9]+[\._]?[a-z0-9]+[@](\w+[.])+\w{2,3}$'
            if not re.fullmatch(r, email):
                raise AccessManagementException("Email invalid")
        if num_emails < 1 or num_emails > 5:
            raise AccessManagementException("JSON Decode Error - Email list invalid")