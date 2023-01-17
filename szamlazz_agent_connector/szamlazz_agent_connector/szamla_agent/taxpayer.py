import inspect

from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.constant.tax_payer_constant import TaxPayerConstant
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.szamla_agent_request import SzamlaAgentRequest
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.szamla_agent_util import SzamlaAgentUtil


class Taxpayer:

    def __init__(self, tax_payer_id='', tax_payer_type=TaxPayerConstant.TAXPAYER_WE_DONT_KNOW):
        self.tax_payer_id = tax_payer_id
        self.tax_payer_type = tax_payer_type

    def get_default(self):
        return TaxPayerConstant.TAXPAYER_WE_DONT_KNOW

