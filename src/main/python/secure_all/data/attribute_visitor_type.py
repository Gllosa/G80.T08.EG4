from .attribute import Attribute


class VisitorType(Attribute):
    def __init__(self, attr_value):
        super().__init__(attr_value, r'(Resident|Guest)', "type of visitor invalid")
        self.attr_value = self._validate(attr_value)
