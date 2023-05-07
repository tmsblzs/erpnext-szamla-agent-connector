from unittest.mock import patch

from frappe.tests.utils import FrappeTestCase
from szamlazz_agent_connector.szamlazz_agent_connector.model.document.document import Document
from szamlazz_agent_connector.szamlazz_agent_connector.service.request_sender import RequestSender
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.szamla_agent import SzamlaAgent
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.szamla_agent_request import SzamlaAgentRequest


@patch("szamlazz_agent_connector.szamlazz_agent_connector.service.request_sender.RequestXmlBuilder")
@patch("szamlazz_agent_connector.szamlazz_agent_connector.service.request_sender.CurlService")
class RequestSenderTestCase(FrappeTestCase):
    def setUp(self) -> None:
        self._sut = RequestSender()

    def test_xml_builder_build_xml_should_call(
            self,
            curl_service_mock,
            request_xml_builder_mock
            ):
        self._setup_sut(curl_service_mock)
        self._setup_request_xml_builder(request_xml_builder_mock)
        self._setup_curl_service(curl_service_mock)
        request = self._create_szamla_agent_request()

        self._sut.send(request)

        request_xml_builder_mock.build \
            .assert_called_once_with(request)

    def test_curl_service_make_call(
            self,
            curl_service_mock,
            request_xml_builder_mock
            ):
        RETURN_VALUE = "test"
        self._setup_sut(curl_service_mock)
        self._setup_request_xml_builder(request_xml_builder_mock, RETURN_VALUE)
        self._setup_curl_service(curl_service_mock)
        request = self._create_szamla_agent_request()

        self._sut.send(request)

        curl_service_mock.make_call \
            .assert_called_once_with(request.agent, request.entity, RETURN_VALUE)

    def _setup_request_xml_builder(self, request_xml_builder_mock, return_value=None):
        if return_value is None:
            return_value = ""
        request_xml_builder_mock.build.return_value = return_value

    def _setup_curl_service(self, curl_service_mock):
        curl_service_mock.make_call.return_value = ""

    def _setup_sut(self, curl_service_mock):
        self._sut._curl_service = curl_service_mock

    def _create_szamla_agent_request(self):
        agent = SzamlaAgent("", "", "")
        entity = Document()
        request = SzamlaAgentRequest(agent, None, entity)
        return request

