import unittest
from unittest.mock import patch, Mock

from frappe.tests.utils import FrappeTestCase
from szamlazz_agent_connector.szamlazz_agent_connector.model.document.invoice.invoice import Invoice
from szamlazz_agent_connector.szamlazz_agent_connector.model.document.invoice.reverse_invoice import ReverseInvoice
from szamlazz_agent_connector.szamlazz_agent_connector.service.request_sender import RequestSender
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.document_generate import document_generate
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.szamla_agent_request import SzamlaAgentRequest
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.szamla_agent_request_type import \
    SzamlaAgentRequestType


class DocumentGenerateInvoiceTestCase(FrappeTestCase):
    @patch("szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.document_generate.RequestSender")
    @patch("szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.document_generate.SzamlaAgentRequestHelper")
    def test_call_request_helper_create(self, mock_szamla_agent_request_helper, mock_request_sender):
        entity = self._create_invoice()
        mock_szamla_agent_request_helper.create = Mock()

        document_generate(entity)

        mock_szamla_agent_request_helper\
            .create.assert_called_with(SzamlaAgentRequestType.INVOICE, entity)

    @patch.object(RequestSender, "send")
    @patch("szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.document_generate.SzamlaAgentRequestHelper")
    def test_request_sender(self, mock_szamla_agent_request_helper, mock_request_sender_send):
        entity = self._create_invoice()
        request = self._create_szamla_agent_request(entity)
        mock_szamla_agent_request_helper.create = Mock(return_value=request)

        document_generate(entity)

        mock_request_sender_send.assert_called_with(request)

    def _create_invoice(self):
        return Invoice(None, None)

    def _create_szamla_agent_request(self, entity):
        return SzamlaAgentRequest(None, None, entity)


class DocumentGenerateReverseInvoiceTestCase(FrappeTestCase):
    @patch("szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.document_generate.RequestSender")
    @patch("szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.document_generate.SzamlaAgentRequestHelper")
    def test_call_request_helper_create(self, mock_szamla_agent_request_helper, mock_request_sender):
        entity = self._create_reverse_invoice()
        mock_szamla_agent_request_helper.create = Mock()

        document_generate(entity)

        mock_szamla_agent_request_helper\
            .create.assert_called_with(SzamlaAgentRequestType.REVERSE_INVOICE, entity)

    @patch.object(RequestSender, "send")
    @patch("szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.document_generate.SzamlaAgentRequestHelper")
    def test_request_sender(self, mock_szamla_agent_request_helper, mock_request_sender_send):
        entity = self._create_reverse_invoice()
        request = self._create_szamla_agent_request(entity)
        mock_szamla_agent_request_helper.create = Mock(return_value=request)

        document_generate(entity)

        mock_request_sender_send.assert_called_with(request)

    def _create_reverse_invoice(self):
        return ReverseInvoice()

    def _create_szamla_agent_request(self, entity):
        return SzamlaAgentRequest(None, None, entity)
