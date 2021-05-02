from .attribute import Attribute


class AccessCode(Attribute):
    def __init__(self, attr_value):
        super().__init__(attr_value, '[0-9a-f]{32}', "access code invalid")
        self.attr_value = self._validate(attr_value)
