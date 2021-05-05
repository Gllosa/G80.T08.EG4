import json
from secure_all.exception.access_management_exception import AccessManagementException


class JsonStore:
    _FILE_PATH = ""
    _ID_FIELD = ""

    def __init__(self):
        self._data_list = []

    def load_store(self):
        try:
            with open(self._FILE_PATH, "r", encoding="utf-8", newline="") as file:
                self._data_list = json.load(file)
        except FileNotFoundError as ex:
            self._data_list = []
        except json.JSONDecodeError as ex:
            raise AccessManagementException("JSON Decode Error - Wrong JSON Format") from ex
        return self._data_list

    def save_store(self):
        try:
            with open(self._FILE_PATH, "w", encoding="utf-8", newline="") as file:
                json.dump(self._data_list, file, indent=2)
        except FileNotFoundError as ex:
            raise AccessManagementException("Wrong file or file path") from ex

    def add_item(self, item):
        self.load_store()
        self._data_list.append(item.__dict__)
        self.save_store()

    def find_item(self, key):
        self.load_store()
        for item in self._data_list:
            if item[self._ID_FIELD] == key:
                return item

    def empty_store(self):
        pass
