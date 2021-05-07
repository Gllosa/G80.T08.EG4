"""Module"""
from .attribute import Attribute


class Email(Attribute):
    """Clase Email"""
    def __init__(self, attr_value):
        regex_sintax = r'^[a-z0-9]+[\._]?[a-z0-9]+[@](\w+[.])+\w{2,3}$'
        error_message = "Email invalid"
        super().__init__(attr_value, regex_sintax, error_message)
        self.attr_value = self._validate(attr_value)
