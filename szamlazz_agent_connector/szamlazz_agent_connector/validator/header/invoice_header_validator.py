from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.szamla_agent_util import SzamlaAgentUtil
from szamlazz_agent_connector.szamlazz_agent_connector.validator.base_validator import BaseValidator


class InvoiceHeaderValidator(BaseValidator):
    def __init__(self):
        self._required_fields = {
            'invoice_date': "",
            'fulfillment': "",
            'paymentDue': "",
            'paymentMethod': "",
            'currency': "",
            'language': "",
            'buyer': "",
            'items': ""
        }

    def _check_field(self, field, value):
        if hasattr(self, field):
            required = True if field in self._required_fields else False
            if field == 'issueDate' \
                    or field == 'fulfillment' \
                    or field == 'paymentDate':
                SzamlaAgentUtil.check_date_field(field, value, required, type(self).__name__)
            elif field == 'exchangeRate' \
                    or field == 'correctionToPay':
                SzamlaAgentUtil.check_float_field(field, value, required, type(self).__name__)
            elif field == 'proforma' \
                    or field == 'deliveryNote' \
                    or field == 'prePayment' \
                    or field == 'final' \
                    or field == 'reverse' \
                    or field == 'paid' \
                    or field == 'profitVat' \
                    or field == 'corrective':
                SzamlaAgentUtil.check_bool_field(field, value, required, type(self).__name__)
            elif field == 'paymentMehtod' \
                    or field == 'currency' \
                    or field == 'comment' \
                    or field == 'exchangeBank' \
                    or field == 'orderNumber' \
                    or field == 'correctivedNumber' \
                    or field == 'extraLogo' \
                    or field == 'prefix' \
                    or field == 'invoiceNumber':
                SzamlaAgentUtil.check_str_field(field, value, required, type(self).__name__)
            return value
