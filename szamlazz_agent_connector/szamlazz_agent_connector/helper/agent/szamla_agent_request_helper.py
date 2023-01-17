from szamlazz_agent_connector.szamlazz_agent_connector.helper.agent.szamla_agent_api_helper import SzamlaAgentApiHelper
from szamlazz_agent_connector.szamlazz_agent_connector.model.document.document import Document
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.szamla_agent_request import SzamlaAgentRequest


class SzamlaAgentRequestHelper:
    @staticmethod
    def create(request_type, entity: Document):
        agent = SzamlaAgentApiHelper.create()
        return SzamlaAgentRequest(agent, request_type, entity)
