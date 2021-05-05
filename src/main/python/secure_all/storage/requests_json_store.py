from .json_store import JsonStore
from secure_all.cfg.access_manager_config import JSON_FILES_PATH
from secure_all.exception.access_management_exception import AccessManagementException

class RequestJsonStore(JsonStore):
    _FILE_PATH = JSON_FILES_PATH + "storeRequest.json"
    _ID_FIELD = "_AccessRequest__id_document"

    def add_item(self, item):
        if not self.find_item(item.id_document) is None:
            raise AccessManagementException("id_docuemnt found in storeRequest")
        return super().add_item(item)

