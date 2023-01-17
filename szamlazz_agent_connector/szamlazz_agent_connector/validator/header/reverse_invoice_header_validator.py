from szamlazz_agent_connector.szamlazz_agent_connector.model.szamla_agent_util import SzamlaAgentUtil
from szamlazz_agent_connector.szamlazz_agent_connector.validator.base_validator import BaseValidator


class ReverseInvoiceHeaderValidator(BaseValidator):
    def __init__(self):
        self._required_fields = {'invoiceNumber': ''}

    def _check_field(self, field, value):
        if hasattr(self, field):
            required = True if field in self._required_fields else False
            if field == 'issue_date' or field == 'fulfillment':
                SzamlaAgentUtil.check_date_field(field, value, required, type(self).__name__)
            if field == 'invoice_number':
                SzamlaAgentUtil.check_str_field(field, value, type(self).__name__)
        return value

