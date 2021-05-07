"""Module"""
from .attribute import Attribute


class VisitorType(Attribute):
    """Clase para validar el tipo de visitante"""
    def __init__(self, attr_value):
        super().__init__(attr_value, r'(Resident|Guest)', "type of visitor invalid")
        self.attr_value = self._validate(attr_value)
