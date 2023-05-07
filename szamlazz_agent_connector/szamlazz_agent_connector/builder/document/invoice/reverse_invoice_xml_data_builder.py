from szamlazz_agent_connector.szamlazz_agent_connector.builder.document.invoice.base_xml_data_builder import \
    BaseXmlDataBuilder
from szamlazz_agent_connector.szamlazz_agent_connector.model.constant.xml_schema import XmlSchema
from szamlazz_agent_connector.szamlazz_agent_connector.model.document.invoice.reverse_invoice import ReverseInvoice
from szamlazz_agent_connector.szamlazz_agent_connector.model.exception.szamla_agent_exception import \
    SzamlaAgentException


class ReverseInvoiceXmlDataBuilder(BaseXmlDataBuilder):
    def build_xml_data(self, request, invoice: ReverseInvoice):
        xml_name = invoice.xml_name
        if xml_name == XmlSchema.XML_SCHEMA_CREATE_REVERSE_INVOICE:
            data = self._build_fields_data(request, invoice, ('beallitasok', 'fejlec'))
        else:
            raise SzamlaAgentException(SzamlaAgentException.XML_SCHEMA_TYPE_NOT_EXISTS + f": {xml_name}")

        return data
