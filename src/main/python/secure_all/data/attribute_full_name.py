"""Module"""
from .attribute import Attribute


class FullName(Attribute):
    """Clase para validar el nombre"""
    def __init__(self, attr_value):
        super().__init__(attr_value, r'^[A-Za-z0-9]+(\s[A-Za-z0-9]+)+', "Invalid full name")
        self.attr_value = self._validate(attr_value)
