from datetime import datetime

from .json_store import JsonStore
from secure_all.cfg.access_manager_config import JSON_FILES_PATH
from secure_all.exception.access_management_exception import AccessManagementException

from ..data.attribute_key import Key


class KeysJsonStore(JsonStore):
    """Extends json store"""
    _FILE_PATH = JSON_FILES_PATH + "storeKeys.json"
    _ID_FIELD = "_AccessKey__key"

    def is_valid(self, key_to_validate):
        item = self.find_item(Key(key_to_validate).value)
        if item is None:
            raise AccessManagementException("key is not found or is expired")

        justnow = datetime.utcnow()
        justnow_timestamp = datetime.timestamp(justnow)
        if item["_AccessKey__expiration_date"] > justnow_timestamp or \
                item["_AccessKey__expiration_date"] == 0:
            return True

        raise AccessManagementException("key is not found or is expired")
