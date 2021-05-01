from attribute import Attribute


class FullName(Attribute):
    def __init__(self, attr_value):
        self._validation_pattern = r'^[A-Za-z0-9]+(\s[A-Za-z0-9]+)+'
        self._error_message = "Email invalid"
        self.attr_value = self._validate(attr_value)
