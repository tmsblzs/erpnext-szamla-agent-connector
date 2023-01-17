from szamlazz_agent_connector.szamlazz_agent_connector.model.constant.invoice_constant import InvoiceConstant
from szamlazz_agent_connector.szamlazz_agent_connector.model.constant.xml_schema import XmlSchema
from szamlazz_agent_connector.szamlazz_agent_connector.model.document.invoice.invoice import Invoice
from szamlazz_agent_connector.szamlazz_agent_connector.model.header.reverse_invoice_header import \
    ReverseInvoiceHeader


class ReverseInvoice(Invoice):
    def __init__(self, invoice_type=InvoiceConstant.INVOICE_TYPE_P_INVOICE):
        super().__init__(None, None)
        self._file_name = 'action-szamla_agent_st'
        self._xml_name = XmlSchema.XML_SCHEMA_CREATE_REVERSE_INVOICE
        self._xsd_dir = 'agentst'

        if invoice_type:
            self._header = ReverseInvoiceHeader(invoice_type)
