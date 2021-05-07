"""Module"""
from .attribute import Attribute


class Key(Attribute):
    """Clase para validar llave"""
    def __init__(self, attr_value):
        super().__init__(attr_value, r'[0-9a-f]{64}', "key invalid")
        self._attr_value = self._validate(attr_value)
