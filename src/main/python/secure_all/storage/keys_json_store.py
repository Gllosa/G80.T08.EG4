"""Module"""
from datetime import datetime

from secure_all.cfg.access_manager_config import JSON_FILES_PATH
from secure_all.exception.access_management_exception import AccessManagementException

from .json_store import JsonStore
from ..data.attribute_key import Key


class KeysJsonStore(JsonStore):
    """Extends json store"""
    _FILE_PATH = JSON_FILES_PATH + "storeKeys.json"
    _ID_FIELD = "_AccessKey__key"
    _INVALID_ITEM = "Invalid item"
    KEY_NOT_FOUND_ERROR = "key is not found or is expired"

    def is_valid(self, key_to_validate):
        """Valida una llave"""
        item = self.find_item(Key(key_to_validate).value)
        if item is None:
            raise AccessManagementException(self.KEY_NOT_FOUND_ERROR)

        justnow = datetime.utcnow()
        justnow_timestamp = datetime.timestamp(justnow)
        if item["_AccessKey__expiration_date"] > justnow_timestamp or \
                item["_AccessKey__expiration_date"] == 0:
            return True

        raise AccessManagementException(self.KEY_NOT_FOUND_ERROR)

    def add_item(self, item):
        """Añade un elemento a los datos que se guardan posteriormente"""
        from secure_all.data.access_key import AccessKey
        if not isinstance(item, AccessKey):
            raise AccessManagementException(self._INVALID_ITEM)
        return super().add_item(item)
