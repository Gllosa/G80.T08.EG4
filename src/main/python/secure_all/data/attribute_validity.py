"""Module"""
from secure_all.exception.access_management_exception import AccessManagementException
from .attribute import Attribute


class Validity(Attribute):
    """Clase para validar la validez"""
    def __init__(self, attr_value, guest_type):
        super().__init__(attr_value, r'', "days invalid")
        self.guest_type = guest_type
        self.attr_value = self._validate(attr_value)

    def _validate(self, attr_value):
        if not isinstance(self.value, int):
            raise AccessManagementException(self._error_message)
        if (self.guest_type == "Resident" and self.value == 0) or (
                self.guest_type == "Guest" and 2 <= self.value <= 15):
            return True
        raise AccessManagementException(self._error_message)
