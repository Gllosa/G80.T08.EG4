"""Module"""
from secure_all.cfg.access_manager_config import JSON_FILES_PATH
from secure_all.exception.access_management_exception import AccessManagementException
from .json_store import JsonStore


class RequestJsonStore(JsonStore):
    """Clase para manejar los json de las requests"""
    _FILE_PATH = JSON_FILES_PATH + "storeRequest.json"
    _ID_FIELD = "_AccessRequest__id_document"
    _ERROR_ID_FOUND = "id_document found in storeRequest"
    _INVALID_ITEM = "Invalid item"

    def add_item(self, item):
        """Añade un elemento"""
        from secure_all.data.access_request import AccessRequest
        if not isinstance(item, AccessRequest):
            raise AccessManagementException(self._INVALID_ITEM)
        if not self.find_item(item.id_document) is None:
            raise AccessManagementException(self._ERROR_ID_FOUND)
        return super().add_item(item)
