from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.szamla_agent_util import SzamlaAgentUtil
from szamlazz_agent_connector.szamlazz_agent_connector.validator.base_validator import BaseValidator


class BuyerValidator(BaseValidator):
    def __init__(self):
        self._required_fields = {'name': "", 'zip': "", 'city': "", 'address': ""}

    def _check_field(self, field, value):
        if hasattr(self, field):
            required = True if field in self._required_fields else False
            if field == 'taxPayer':
                SzamlaAgentUtil.check_int_field(field, value, required, type(self).__name__)
            elif field == 'sendEmail':
                SzamlaAgentUtil.check_bool_field(field, value, required, type(self).__name__)
            elif field == 'id' \
                    or field == 'email' \
                    or field == 'name' \
                    or field == 'country' \
                    or field == 'zipCode' \
                    or field == 'city' \
                    or field == 'address' \
                    or field == 'taxNumber' \
                    or field == 'taxNumberEU' \
                    or field == 'postalName' \
                    or field == 'postalCountry' \
                    or field == 'postalZip' \
                    or field == 'postalCity' \
                    or field == 'postalAddress' \
                    or field == 'signatoryName' \
                    or field == 'phone' \
                    or field == 'comment':
                SzamlaAgentUtil.check_str_field(field, value, required, type(self).__name__)
        return value
