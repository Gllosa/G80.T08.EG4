"""Module"""
import json
from secure_all.exception.access_management_exception import AccessManagementException


class JsonStore:
    """Clase base para manejar los Jsons"""
    _FILE_PATH = ""
    _ID_FIELD = ""
    JSON_DECODE_ERROR = "JSON Decode Error - Wrong JSON Format"
    WRONG_FILE_ERROR = "Wrong file or file path"

    def __init__(self):
        """Init para el manejador de json"""
        self._data_list = []

    def load_store(self):
        """Carga los datos desde un archivo"""
        try:
            with open(self._FILE_PATH, "r", encoding="utf-8", newline="") as file:
                self._data_list = json.load(file)
        except FileNotFoundError as ex:
            self._data_list = []
        except json.JSONDecodeError as ex:
            raise AccessManagementException(self.JSON_DECODE_ERROR) from ex
        return self._data_list

    def save_store(self):
        """Guarda en el json los datos"""
        try:
            with open(self._FILE_PATH, "w", encoding="utf-8", newline="") as file:
                json.dump(self._data_list, file, indent=2)
        except FileNotFoundError as ex:
            raise AccessManagementException(self.WRONG_FILE_ERROR) from ex

    def add_item(self, item):
        """Añade un elemento a los datos que se guardan posteriormente"""
        self.load_store()
        self._data_list.append(item.__dict__)
        self.save_store()

    def find_item(self, key):
        """Devuelve un determinado objeto en el Json"""
        self.load_store()
        for item in self._data_list:
            if item[self._ID_FIELD] == key:
                return item
        return None
