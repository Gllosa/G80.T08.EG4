import re
from secure_all.exception.access_management_exception import AccessManagementException


class Attribute:
    """Class Attribute for representing a generic attribute"""
    """
    # Default value
    _attr_value = ""
    # Regex validation pattern
    _validation_pattern = r""
    # Default error message
    _error_message = ""
    """
    def __init__(self, value, pattern, message):
        self._attr_value = value
        self._validation_pattern = pattern
        self._error_message = message

    def _validate(self, attr_value):
        if not isinstance(attr_value, str):
            raise AccessManagementException(self._error_message)
        if not re.fullmatch(self._validation_pattern, attr_value):
            raise AccessManagementException(self._error_message)
        return attr_value

    @property
    def value(self):
        return self._attr_value

    @value.setter
    def value(self, attr_value):
        self._attr_value = attr_value

