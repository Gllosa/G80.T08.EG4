"""Module"""
from .json_parser import JsonParser


class KeyJsonParser(JsonParser):
    """Clase para manejar los Jsons de las llaves"""
    keys = ["AccessCode", "DNI", "NotificationMail"]
