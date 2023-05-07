from szamlazz_agent_connector.szamlazz_agent_connector.model.document.invoice.invoice import Invoice
from szamlazz_agent_connector.szamlazz_agent_connector.model.exception.szamla_agent_exception import \
    SzamlaAgentException


class BaseXmlDataBuilder:
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
