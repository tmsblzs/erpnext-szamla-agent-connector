from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.szamla_agent_request import SzamlaAgentRequest
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.taxpayer import Taxpayer


class TaxpayerXmlDataBuilder:
    def build_xml_data(self, request: SzamlaAgentRequest, taxpayer: Taxpayer):
        from szamlazz_agent_connector.szamlazz_agent_connector.builder.build_xml_data import build_xml_data
        data = {
            'beallitasok': build_xml_data(request, request),
            'torzsszam': taxpayer.tax_payer_id
        }

        return data
