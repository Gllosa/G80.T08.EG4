from .attribute import Attribute
from secure_all.access_management_exception import AccessManagementException


class KeyLabels(Attribute):
    def __init__(self, labels_dict):
        super().__init__(labels_dict, '', "JSON Decode Error - Wrong label")
        self.labels_dict = labels_dict
        self.attr_value = self._validate(labels_dict)

    def _validate(self, labels_dict):
        if not ("AccessCode" in labels_dict.keys()):
            raise AccessManagementException(self._error_message)
        if not ("DNI" in labels_dict.keys()):
            raise AccessManagementException(self._error_message)
        if not ("NotificationMail" in labels_dict.keys()):
            raise AccessManagementException(self._error_message)
        return True
