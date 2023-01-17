from szamlazz_agent_connector.szamlazz_agent_connector.builder.setting_xml_data_builder import SettingXmlDataBuilder
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.szamla_agent_request import SzamlaAgentRequest
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.taxpayer import Taxpayer
from szamlazz_agent_connector.szamlazz_agent_connector.validator.taxpayer_validator import TaxpayerValidator


class TaxpayerXmlDataBuilder:
    def __init__(self, setting_builder: SettingXmlDataBuilder, validator: TaxpayerValidator):
        self._setting_builder = setting_builder
        self._validator = validator

    def build_xml_data(self, request: SzamlaAgentRequest, taxpayer: Taxpayer):
        self._validator.check_fields(taxpayer)
        data = {
            'beallitasok': self._setting_builder.build_xml_data(request, request),
            'torzsszam': taxpayer.tax_payer_id
        }

        return data
