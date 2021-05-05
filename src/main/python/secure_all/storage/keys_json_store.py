from .json_store import JsonStore
from secure_all.cfg.access_manager_config import JSON_FILES_PATH
from secure_all.exception.access_management_exception import AccessManagementException


class KeysJsonStore(JsonStore):
    """Extends json store"""
    ID_FIELD = "_Access__key"
    ACCESS_CODE = "_AccessKey_access_code"
    DNI = "_AccessKey__dni"
    MAIL_LIST = "_AccessKey_notification_emails"
    INVALI_ITEM = "Invalid item to be sotored as a key"
    KEY_ALREADY_STORED = "Key already found in storeRequest"

    _FILE_PATH = JSON_FILES_PATH + "storeKeys.json"
    _ID_FIELD = ID_FIELD

    # def add_item(self, item):
    #     """Implementing the restrictions related to avoid duplicated keys"""
    #     from secure_all.data.access_key import AccessKey
    #
    #     if not isinstance(item, AccessKey):
    #         raise AccessManagementException(self.INVALI_ITEM)
    #
    #     if not self.find_item(item.key) is None:
    #         raise AccessManagementException(self.KEY_ALREADY_STORED)
    #
    #     return super().add_item(item)
