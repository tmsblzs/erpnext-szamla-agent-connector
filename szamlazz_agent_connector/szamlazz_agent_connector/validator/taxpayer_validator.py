from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.szamla_agent_util import SzamlaAgentUtil
from szamlazz_agent_connector.szamlazz_agent_connector.validator.base_validator import BaseValidator


class Taxpayer(BaseValidator):
    def __init__(self):
        self._required_fields = {'taxPayerId'}

    def _check_field(self, field, value):
        if hasattr(self, field):
            required = True if field in self._required_fields else False
            if field == 'taxPayerType':
                SzamlaAgentUtil.check_int_field(field, value, required, type(self).__name__)
            elif field == 'taxPayerId':
                SzamlaAgentUtil.check_str_field_with_reg_exp(field, value, required, type(self).__name__)
