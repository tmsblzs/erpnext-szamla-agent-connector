from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.szamla_agent_util import SzamlaAgentUtil
from szamlazz_agent_connector.szamlazz_agent_connector.validator.base_validator import BaseValidator


class InvoiceItemValidator(BaseValidator):
    def __init__(self):
        self.required_fields = {'name', 'quantity', 'quantityUnit',
                                'netUnitPrice', 'vat', 'netPrice', 'vatAmount', 'grossAmount'}

    def _check_field(self, field, value):
        if hasattr(self, field):
            required = True if field in self.required_fields else False
            if field == 'quantity' \
                    or field == 'netUnitPrice' \
                    or field == 'priceGapVatBase' \
                    or field == 'netPrice' \
                    or field == 'vatAmount' \
                    or field == 'grossAmount':
                SzamlaAgentUtil.check_float_field(field, value, required, type(self).__name__)
            elif field == 'name' \
                    or field == 'id' \
                    or field == 'quantityUnit' \
                    or field == 'vat' \
                    or field == 'comment':
                SzamlaAgentUtil.check_str_field(field, value, required, type(self).__name__)
        return value
