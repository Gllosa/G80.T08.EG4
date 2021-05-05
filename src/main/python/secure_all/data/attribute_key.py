from .attribute import Attribute


class Key(Attribute):

    def __init__(self, attr_value):
        self._validation_pattern = r'[0-9a-f]{64}'
        self._error_message = "key invalid"
        self._attr_value = self._validate(attr_value)
