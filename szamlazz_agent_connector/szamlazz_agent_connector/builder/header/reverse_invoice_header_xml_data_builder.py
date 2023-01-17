from collections import OrderedDict

from szamlazz_agent_connector.szamlazz_agent_connector.model.constant.document_constant import DocumentConstant
from szamlazz_agent_connector.szamlazz_agent_connector.model.exception.szamla_agent_exception import \
    SzamlaAgentException
from szamlazz_agent_connector.szamlazz_agent_connector.model.header.reverse_invoice_header import \
    ReverseInvoiceHeader
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.szamla_agent_request import SzamlaAgentRequest
from szamlazz_agent_connector.szamlazz_agent_connector.validator.header.reverse_invoice_header_validator import \
    ReverseInvoiceHeaderValidator


class ReverseInvoiceXmlDataBuilder:
    def __init__(self, validator: ReverseInvoiceHeaderValidator):
        self._validator = validator

    def build_xml_data(self, request: SzamlaAgentRequest, reverse_invoice: ReverseInvoiceHeader):
        if not request:
            raise SzamlaAgentException(SzamlaAgentException.XML_DATA_NOT_AVAILABLE)

        self._validator.check_fields(reverse_invoice)

        data = OrderedDict([
            ("szamlaszam", reverse_invoice.invoice_number)
        ])
        if reverse_invoice.issue_date:
            data['keltDatum'] = reverse_invoice.issue_date
        if reverse_invoice.fulfillment:
            data['teljesitesDatum'] = reverse_invoice.fulfillment
        data['tipus'] = DocumentConstant.DOCUMENT_TYPE_REVERSE_INVOICE_CODE
        if reverse_invoice.invoice_template:
            data['szamlaSablon'] = reverse_invoice.invoice_template

        return data
