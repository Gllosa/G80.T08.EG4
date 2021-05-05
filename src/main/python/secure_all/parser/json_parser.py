import json
from secure_all.exception.access_management_exception import AccessManagementException


class JsonParser:
    keys = []

    def __init__(self, file):
        self._file = file
        self._json_content = self._parse_json_file()
        self._validate_json()

    def _parse_json_file(self):
        try:
            with open(self._file, "r", encoding="utf-8", newline="") as file:
                data = json.load(file)
        except FileNotFoundError as ex:
            raise AccessManagementException("Wrong file or file path") from ex
        except json.JSONDecodeError as ex:
            raise AccessManagementException("JSON Decode Error - Wrong JSON Format") from ex
        return data

    def _validate_json(self):
        for key in self.keys:
            if key not in self._json_content:
                raise AccessManagementException("JSON Decode Error - Wrong label")

    @property
    def json_content(self):
        return self._json_content
