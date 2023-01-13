from szamlazz_agent_connector.szamlazz_agent_connector.builder.header.invoice_header_xml_builder import \
    InvoiceHeaderXmlBuilder
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.constant.xml_schema import XmlSchema
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.document.invoice.invoice import Invoice
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.exception.szamla_agent_exception import \
    SzamlaAgentException


class InvoiceXmlBuilder():
    def __init__(self):
        self._invoice = None
        self._header_xml_builder = InvoiceHeaderXmlBuilder()

    def build_xml_data(self, request, invoice: Invoice):
        self._invoice = invoice
        xml_name = request.xml_name
        if xml_name == XmlSchema.XML_SCHEMA_CREATE_INVOICE:
            data = self._build_fields_data(request,
                                           ('beallitasok', 'fejlec', 'elado', 'vevo', 'fuvarlevel', 'tetelek'))
        elif xml_name == XmlSchema.XML_SCHEMA_DELETE_PROFORMA:
            data = self._build_fields_data(request, ('beallitasok', 'fejlec'))
        elif xml_name == XmlSchema.XML_SCHEMA_CREATE_REVERSE_INVOICE:
            data = self._build_fields_data(request, ('beallitasok', 'fejlec', 'elado', 'vevo'))
        elif xml_name == XmlSchema.XML_SCHEMA_PAY_INVOICE:
            data = self._build_fields_data(request, 'beallitasok')
            data = {**data, **self._build_credits_xml_data()}
        elif xml_name == XmlSchema.XML_SCHEMA_REQUEST_INVOICE_XML \
                or XmlSchema.XML_SCHEMA_REQUEST_INVOICE_PDF:
            settings = self._build_fields_data(request, 'beallitasok')
            data = settings['beallitasok']
        else:
            raise SzamlaAgentException(SzamlaAgentException.XML_SCHEMA_TYPE_NOT_EXISTS + f": {xml_name}")

        return data

    def _build_fields_data(self, request, fields):
        data = {}

        for key in fields:
            if key == 'beallitasok':
                value = request.agent.setting.build_xml_data(request)
            elif key == 'fejlec':
                value = self._header_xml_builder.build_xml_data(self._invoice.header)
            elif key == 'tetelek':
                value = self._build_xml_items_data()
            elif key == 'elado':
                value = self.seller.build_xml_data(request) if self.seller else []
            elif key == 'vevo':
                value = self.buyer.build_xml_data(request) if self.buyer else []
            elif key == 'fuvarlevel':
                value = None
            else:
                raise SzamlaAgentException(SzamlaAgentException.XML_KEY_NOT_EXISTS + f": {key}")

            if value:
                data[key] = value

        return data

    def _build_xml_items_data(self):
        data = {}
        count = 0
        for item in self.items:
            count += 1
            data[f"item{count}"] = item.build_xml_data()
        return data

    def _build_credits_xml_data(self):
        data = {}
        count = 0
        for item in self._credit_notes:
            count += 1
            data[f"note{count}"] = item.build_xml_data()
        return data
