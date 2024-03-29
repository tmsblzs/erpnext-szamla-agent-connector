from szamlazz_agent_connector.szamlazz_agent_connector.builder.agent.request_xml_builder import RequestXmlBuilder
from szamlazz_agent_connector.szamlazz_agent_connector.service.curl_service import CurlService
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.szamla_agent_request import SzamlaAgentRequest


class RequestSender:
    def __init__(self):
        self.xml_file_path = ''
        self._curl_service = CurlService()

    def send(self, request: SzamlaAgentRequest):
        xml_str = RequestXmlBuilder.build(request)
        agent = request.agent
        entity = request.entity
        response = self._curl_service.make_call(agent, entity, xml_str)
        return response
