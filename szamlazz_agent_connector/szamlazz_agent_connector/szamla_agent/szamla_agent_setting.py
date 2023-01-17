from collections import OrderedDict

from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.constant.response_constant import ResponseConstant
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.constant.xml_schema import XmlSchema
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.exception.szamla_agent_exception import \
    SzamlaAgentException
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.response.szamla_agent_response import \
    SzamlaAgentResponse
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.szamla_agent_request import SzamlaAgentRequest


class SzamlaAgentSetting:
    DOWNLOAD_COPIES_COUNT = 1
    API_KEY_LENGTH = 42

    def __init__(self,
                 username,
                 password,
                 api_key,
                 download_pdf=True,
                 copies_count=DOWNLOAD_COPIES_COUNT,
                 response_type=ResponseConstant.RESULT_AS_TEXT,
                 aggregator=''):
        self.username = username
        self.password = password
        self.api_key = api_key
        self.download_pdf = download_pdf
        self.copies_count = copies_count
        self.response_type = response_type
        self.aggregator = aggregator
        self.guardian = False
        self.keychain = ""

    def build_xml_data(self, request: SzamlaAgentRequest):
        settings = ('felhasznalo', 'jelszo', 'szamlaagentkulcs')

        xml_name = request.xmlName
        if xml_name == XmlSchema.XML_SCHEMA_CREATE_INVOICE:
            data = self.__build_fields_data(request,
                                            settings + ('eszamla', 'kulcstartojelszo', 'szamlaLetoltes',
                                                        'szamlaLetoltesPld', 'valaszVerzio', 'aggregator', 'guardian'))
        elif xml_name == XmlSchema.XML_SCHEMA_DELETE_PROFORMA:
            data = self.__build_fields_data(request, settings)
        elif xml_name == XmlSchema.XML_SCHEMA_CREATE_REVERSE_INVOICE:
            data = self.__build_fields_data(request,
                                            settings + ('eszamla', 'kulcstartojelszo', 'szamlaLetoltes',
                                                        'szamlaLetoltesPld', 'aggregator', 'guardian', 'valaszVerzio'))
        elif xml_name == XmlSchema.XML_SCHEMA_PAY_INVOICE:
            data = self.__build_fields_data(request, settings + ('szamlaszam', 'additiv', 'aggregator', 'valaszVerzio'))
        elif xml_name == XmlSchema.XML_SCHEMA_REQUEST_INVOICE_XML:
            data = self.__build_fields_data(request, settings + ('szamlaszam', 'rendelesSzam', 'pdf'))
        elif xml_name == XmlSchema.XML_SCHEMA_REQUEST_INVOICE_PDF:
            data = self.__build_fields_data(request, settings + ('szamlaszam', 'rendelesSzam', 'valaszVerzio'))
        elif xml_name == XmlSchema.XML_SCHEMA_CREATE_INVOICE \
                or xml_name == XmlSchema.XML_SCHEMA_CREATE_REVERSE_RECEIPT \
                or xml_name == XmlSchema.XML_SCHEMA_GET_RECEIPT:
            data = self.__build_fields_data(request, settings + ('pdfLetoltes'))
        elif xml_name == XmlSchema.XML_SCHEMA_SEND_RECEIPT \
                or xml_name == XmlSchema.XML_SCHEMA_TAXPAYER:
            data = self.__build_fields_data(request, settings)
        else:
            raise SzamlaAgentException(SzamlaAgentException.XML_SCHEMA_TYPE_NOT_EXISTS + f": {xml_name}")

        return data

    def __build_fields_data(self, request: SzamlaAgentRequest, fields):
        data = OrderedDict()

        field_data = {
            'felhasznalo': self.username,
            'jelszo': self.password,
            'szamlaagentkulcs': self.api_key,
            'kulcstartojelszo': self.keychain,
            'szamlaLetoltes': self.download_pdf,
            'pdf': self.download_pdf,
            'pdfLetoltes': self.download_pdf,
            'szamlaLetoltesPld': self.copies_count,
            'valaszVerzio': self.response_type,
            'aggregator': self.aggregator,
            'guardian': self.guardian,
            'eszamla': 'true' if request.entity.header.is_e_invoice() else 'false',
            'additiv': request.entity.is_additive,
            'szamlaszam': request.entity.header.invoice_number,
            'rendelesSzam': request.entity.header.order_number
        }

        for field in fields:
            value = field_data[field]
            if value:
                data[field] = value

        return data
