import frappe
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.szamla_agent_api import SzamlaAgentApi


class SzamlaAgentApiHelper:
    @staticmethod
    def create():
        connection_settings = frappe.get_doc('SzamlazzAgentConnectorSetting')
        return SzamlaAgentApi.create(connection_settings.apikey)
