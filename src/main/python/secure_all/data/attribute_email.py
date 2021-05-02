from .attribute import Attribute


class Email(Attribute):
    def __init__(self, attr_value):
        super().__init__(attr_value, r'^[a-z0-9]+[\._]?[a-z0-9]+[@](\w+[.])+\w{2,3}$', "Email invalid")
        self.attr_value = self._validate(attr_value)
