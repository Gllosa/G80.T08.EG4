"""Module"""
import re

from secure_all.exception.access_management_exception import AccessManagementException
from .attribute import Attribute


class Dni(Attribute):
    """Clase Dni"""
    def __init__(self, attr_value):
        super().__init__(attr_value, r'', "DNI is not valid")
        self.attr_value = self._validate(attr_value)

    def _validate(self, attr_value):
        """RETURN TRUE IF THE DNI IS RIGHT, OR FALSE IN OTHER CASE"""
        self.validate_dni_syntax(attr_value)
        if not self.validate_dni_character(attr_value):
            raise AccessManagementException(self._error_message)
        return True

    @staticmethod
    def validate_dni_character(dni):
        """Devuelve true si la letra del dni sigue el algortimo"""
        letra_control = {"0": "T", "1": "R", "2": "W", "3": "A", "4": "G", "5": "M",
                         "6": "Y", "7": "F", "8": "P", "9": "D", "10": "X", "11": "B",
                         "12": "N", "13": "J", "14": "Z", "15": "S", "16": "Q", "17": "V",
                         "18": "H", "19": "L", "20": "C", "21": "K", "22": "E"}
        numero_dni = int(dni[0:8])
        clave_letra = str(numero_dni % 23)
        return dni[8] == letra_control[clave_letra]

    @staticmethod
    def validate_dni_syntax(dni):
        """validating the dni syntax"""
        expresion_regex = r'^[0-9]{8}[A-Z]{1}$'
        if re.fullmatch(expresion_regex, dni):
            return True
        raise AccessManagementException("DNI is not valid")
