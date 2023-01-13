import inspect

from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.constant.tax_payer_constant import TaxPayerConstant
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.szamla_agent_request import SzamlaAgentRequest
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.szamla_agent_util import SzamlaAgentUtil


class TaxPayer:

    def __init__(self, tax_payer_id='', tax_payer_type=TaxPayerConstant.TAXPAYER_WE_DONT_KNOW):
        self.tax_payer_id = tax_payer_id
        self.tax_payer_type = tax_payer_type
        self.__required_fields = {'taxPayerId'}

    def get_default(self):
        return TaxPayerConstant.TAXPAYER_WE_DONT_KNOW

    def _check_field(self, field, value):
        if hasattr(self, field):
            required = True if field in self.__required_fields else False
            if field == 'taxPayerType':
                SzamlaAgentUtil.check_int_field(field, value, required, type(self).__name__)
            elif field == 'taxPayerId':
                SzamlaAgentUtil.check_str_field_with_reg_exp(field, value, required, type(self).__name__)

    def _check_fields(self):
        fields = inspect.getmembers(TaxPayer, lambda a: not (inspect.isroutine(a)))
        fields = [a for a in fields if not (a[0].startswith('__') and a[0].endswith('__'))]
        for item in fields:
            self._check_field(item[0], item[1])

    def build_xml_data(self, request: SzamlaAgentRequest):
        self._check_fields()

        data = {
            'beallitasok': request.agent.setting.build_xml_data(request),
            'torzsszam': self.tax_payer_id
        }

        return data
