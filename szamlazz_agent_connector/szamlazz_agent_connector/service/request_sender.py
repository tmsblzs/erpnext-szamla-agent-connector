from html import unescape
from urllib.parse import unquote

from szamlazz_agent_connector.szamlazz_agent_connector.builder.agent.request_xml_builder import RequestXmlBuilder
from szamlazz_agent_connector.szamlazz_agent_connector.builder.query.query_builder import QueryBuilder
from szamlazz_agent_connector.szamlazz_agent_connector.service.curl_service import CurlService
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.szamla_agent_request import SzamlaAgentRequest


class RequestSender:
    def __init__(self):
        self.xml_file_path = ''
        self._xml_builder = RequestXmlBuilder()
        self._curl_service = CurlService()

    def send(self, request: SzamlaAgentRequest):
        xml_str = self._xml_builder.build_xml(request)
        agent = request.agent
        entity = request.entity
        query_str = QueryBuilder.build_query(xml_str, entity.filename)
        response = self._curl_service.make_call(agent, entity, query_str)
        return response
