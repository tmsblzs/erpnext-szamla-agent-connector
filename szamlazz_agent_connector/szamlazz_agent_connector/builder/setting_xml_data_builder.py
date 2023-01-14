from collections import OrderedDict

from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.constant.xml_schema import XmlSchema
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.exception.szamla_agent_exception import \
    SzamlaAgentException
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.szamla_agent_request import SzamlaAgentRequest
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.szamla_agent_setting import SzamlaAgentSetting


class SettingXmlDataBuilder:
    def build_xml_data(self, request: SzamlaAgentRequest, setting: SzamlaAgentSetting):
        fields = ('felhasznalo', 'jelszo', 'szamlaagentkulcs')

        xml_name = request.xml_name
        if xml_name == XmlSchema.XML_SCHEMA_CREATE_INVOICE:
            data = self._build_fields_data(request,
                                           setting,
                                           fields + ('eszamla', 'kulcstartojelszo', 'szamlaLetoltes',
                                                     'szamlaLetoltesPld', 'valaszVerzio', 'aggregator', 'guardian'))
        elif xml_name == XmlSchema.XML_SCHEMA_DELETE_PROFORMA:
            data = self._build_fields_data(request, setting, fields)
        elif xml_name == XmlSchema.XML_SCHEMA_CREATE_REVERSE_INVOICE:
            data = self._build_fields_data(request,
                                           setting,
                                           fields + ('eszamla', 'kulcstartojelszo', 'szamlaLetoltes',
                                                     'szamlaLetoltesPld', 'aggregator', 'guardian', 'valaszVerzio'))
        elif xml_name == XmlSchema.XML_SCHEMA_PAY_INVOICE:
            data = self._build_fields_data(request,
                                           setting,
                                           fields + ('szamlaszam', 'additiv', 'aggregator', 'valaszVerzio'))
        elif xml_name == XmlSchema.XML_SCHEMA_REQUEST_INVOICE_XML:
            data = self._build_fields_data(request, setting, fields + ('szamlaszam', 'rendelesSzam', 'pdf'))
        elif xml_name == XmlSchema.XML_SCHEMA_REQUEST_INVOICE_PDF:
            data = self._build_fields_data(request, setting, fields + ('szamlaszam', 'rendelesSzam', 'valaszVerzio'))
        elif xml_name == XmlSchema.XML_SCHEMA_CREATE_INVOICE \
                or xml_name == XmlSchema.XML_SCHEMA_CREATE_REVERSE_RECEIPT \
                or xml_name == XmlSchema.XML_SCHEMA_GET_RECEIPT:
            data = self._build_fields_data(request, setting, fields + ('pdfLetoltes',))
        elif xml_name == XmlSchema.XML_SCHEMA_SEND_RECEIPT \
                or xml_name == XmlSchema.XML_SCHEMA_TAXPAYER:
            data = self._build_fields_data(request, setting, fields)
        else:
            raise SzamlaAgentException(SzamlaAgentException.XML_SCHEMA_TYPE_NOT_EXISTS + f": {xml_name}")

        return data

    def _build_fields_data(self, request: SzamlaAgentRequest, setting: SzamlaAgentSetting, fields):
        data = OrderedDict()

        field_data = {
            'felhasznalo': setting.username,
            'jelszo': setting.password,
            'szamlaagentkulcs': setting.api_key,
            'kulcstartojelszo': setting.keychain,
            'szamlaLetoltes': setting.download_pdf,
            'pdf': setting.download_pdf,
            'pdfLetoltes': setting.download_pdf,
            'szamlaLetoltesPld': setting.copies_count,
            'valaszVerzio': setting.response_type,
            'aggregator': setting.aggregator,
            'guardian': setting.guardian,
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
