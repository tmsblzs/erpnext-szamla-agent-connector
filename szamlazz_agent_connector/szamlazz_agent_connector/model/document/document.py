from szamlazz_agent_connector.szamlazz_agent_connector.model.currency import Currency
from szamlazz_agent_connector.szamlazz_agent_connector.model.language import Language


class Document:
    @property
    def xml_schema_type(self):
        return self._xml_schema_type

    @property
    def filename(self):
        return self._file_name

    @property
    def xml_name(self):
        return self._xml_name

    @property
    def xsd_dir(self):
        return self._xsd_dir

    @property
    def is_attachments(self):
        return len(self.attachments) > 0

    def __init__(self):
        self._file_name = None
        self._xml_name = None
        self._xsd_dir = None
        self._xml_schema_type = None
        self.header = None
        self.attachments = []


    @staticmethod
    def get_default_currency():
        return Currency.get_default()

    @staticmethod
    def get_default_language():
        return Language.get_default()
