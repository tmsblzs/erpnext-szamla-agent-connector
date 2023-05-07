from szamlazz_agent_connector.szamlazz_agent_connector.builder.document.invoice.base_xml_data_builder import \
    BaseXmlDataBuilder
from szamlazz_agent_connector.szamlazz_agent_connector.model.constant.xml_schema import XmlSchema
from szamlazz_agent_connector.szamlazz_agent_connector.model.document.invoice.invoice import Invoice
from szamlazz_agent_connector.szamlazz_agent_connector.model.exception.szamla_agent_exception import \
    SzamlaAgentException


class InvoiceXmlDataBuilder(BaseXmlDataBuilder):
    def build_xml_data(self, request, invoice: Invoice):
        xml_name = invoice.xml_name
        if xml_name == XmlSchema.XML_SCHEMA_CREATE_INVOICE:
            data = self._build_fields_data(request, invoice,
                                           ('beallitasok', 'fejlec', 'elado', 'vevo', 'fuvarlevel', 'tetelek'))
        elif xml_name == XmlSchema.XML_SCHEMA_DELETE_PROFORMA:
            data = self._build_fields_data(request, invoice, ('beallitasok', 'fejlec'))
        elif xml_name == XmlSchema.XML_SCHEMA_CREATE_REVERSE_INVOICE:
            data = self._build_fields_data(request, invoice, ('beallitasok', 'fejlec', 'elado', 'vevo'))
        elif xml_name == XmlSchema.XML_SCHEMA_PAY_INVOICE:
            data = self._build_fields_data(request, invoice, 'beallitasok')
            data = {**data, **self._build_credits_xml_data()}
        elif xml_name == XmlSchema.XML_SCHEMA_REQUEST_INVOICE_XML \
                or XmlSchema.XML_SCHEMA_REQUEST_INVOICE_PDF:
            settings = self._build_fields_data(request, invoice, 'beallitasok')
            data = settings['beallitasok']
        else:
            raise SzamlaAgentException(SzamlaAgentException.XML_SCHEMA_TYPE_NOT_EXISTS + f": {xml_name}")

        return data

