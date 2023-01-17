from collections import OrderedDict

from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.constant.document_constant import DocumentConstant
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.exception.szamla_agent_exception import \
    SzamlaAgentException
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.header.invoice_header import InvoiceHeader
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.szamla_agent_request import SzamlaAgentRequest
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.szamla_agent_util import SzamlaAgentUtil


class ReverseInvoiceHeader(InvoiceHeader):

    def __init__(self, invoice_type):
        super().__init__(invoice_type)
        self._required_fields = {'invoiceNumber': ''}
        self.reverse_invoice = True
        self.issue_date = None
        self.fulfillment = None

    def __check_field(self, field, value):
        if hasattr(self, field):
            required = True if field in self._required_fields else False
            if field == 'issue_date' or field == 'fulfillment':
                SzamlaAgentUtil.check_date_field(field, value, required, type(self).__name__)
            if field == 'invoice_number':
                SzamlaAgentUtil.check_str_field(field, value, type(self).__name__)
        return value

    def build_xml_data(self, request: SzamlaAgentRequest):
        try:
            if not request:
                raise SzamlaAgentException(SzamlaAgentException.XML_DATA_NOT_AVAILABLE)

            data = OrderedDict([
                ("szamlaszam", self.invoice_number)
            ])
            if self.issue_date:
                data['keltDatum'] = self.issue_date
            if self.fulfillment:
                data['teljesitesDatum'] = self.fulfillment
            data['tipus'] = DocumentConstant.DOCUMENT_TYPE_REVERSE_INVOICE_CODE
            if self.invoice_template:
                data['szamlaSablon'] = self.invoice_template

            self.check_fields()

            return data
        except SzamlaAgentException as e:
            raise e
