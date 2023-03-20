from szamlazz_agent_connector.szamlazz_agent_connector.model.constant.xml_schema import XmlSchema
from szamlazz_agent_connector.szamlazz_agent_connector.model.document.invoice.invoice import Invoice
from szamlazz_agent_connector.szamlazz_agent_connector.model.exception.szamla_agent_exception import \
    SzamlaAgentException


class InvoiceXmlDataBuilder:
    def build_xml_data(self, request, invoice: Invoice):
        xml_name = request.xml_name
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

    def _build_fields_data(self, request, invoice: Invoice, fields):
        data = {}

        for key in fields:
            if key == 'beallitasok':
                from szamlazz_agent_connector.szamlazz_agent_connector.builder.build_xml_data import build_xml_data
                value = build_xml_data(request.agent.setting, request)
            elif key == 'fejlec':
                from szamlazz_agent_connector.szamlazz_agent_connector.builder.build_xml_data import build_xml_data
                value = build_xml_data(invoice.header, request)
            elif key == 'tetelek':
                from szamlazz_agent_connector.szamlazz_agent_connector.builder.build_xml_data import build_xml_data
                value = build_xml_data(invoice.items, request)
            elif key == 'elado':
                from szamlazz_agent_connector.szamlazz_agent_connector.builder.build_xml_data import build_xml_data
                value = build_xml_data(invoice.seller, request) if invoice.seller else []
            elif key == 'vevo':
                from szamlazz_agent_connector.szamlazz_agent_connector.builder.build_xml_data import build_xml_data
                value = build_xml_data(invoice.buyer, request) if invoice.buyer else []
            elif key == 'fuvarlevel':
                value = None
            else:
                raise SzamlaAgentException(SzamlaAgentException.XML_KEY_NOT_EXISTS + f": {key}")

            if value:
                data[key] = value

        return data

    def _build_credits_xml_data(self, invoice: Invoice):
        data = {}
        count = 0
        for item in invoice.credit_notes:
            count += 1
            data[f"note{count}"] = item.build_xml_data()
        return data
