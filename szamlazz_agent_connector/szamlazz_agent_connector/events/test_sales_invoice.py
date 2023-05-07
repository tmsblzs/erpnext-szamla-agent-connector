import frappe
from szamlazz_agent_connector.szamlazz_agent_connector.events.sales_invoice import on_submit

from frappe.tests.utils import FrappeTestCase
from unittest.mock import patch, Mock
from szamlazz_agent_connector.szamlazz_agent_connector.model.document.invoice.invoice import Invoice
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.szamla_agent_request import SzamlaAgentRequest


@patch("szamlazz_agent_connector.szamlazz_agent_connector.events.sales_invoice.AgentInvoiceHelper")
@patch("szamlazz_agent_connector.szamlazz_agent_connector.events.sales_invoice.PdfFileHelper")
@patch("szamlazz_agent_connector.szamlazz_agent_connector.events.sales_invoice.document_generate")
@patch("szamlazz_agent_connector.szamlazz_agent_connector.events.sales_invoice.InvoiceHelper")
@patch("szamlazz_agent_connector.szamlazz_agent_connector.events.sales_invoice.SzamlaAgentResponse")
class TestSalesInvoice(FrappeTestCase):

    def test_call_create_from_sales_invoice(self,
                                            agent_response_mock,
                                            invoice_helper,
                                            document_generate,
                                            pdf_file_helper_mock,
                                            agent_invoice_helper_mock ):
        sales_invoice = frappe.new_doc("Sales Invoice")
        seller = frappe.new_doc("Company")
        buyer = frappe.new_doc("Customer")
        invoice_helper.create_from_sales_invoice.return_value = Invoice(seller, buyer)
        self._setup_document_generate(document_generate)
        self._setup_pdf_file_helper(pdf_file_helper_mock)
        self._setup_agent_invoice_helper(agent_invoice_helper_mock)
        agent_response_mock.handle_response.return_value = Invoice(seller, buyer)

        on_submit(sales_invoice, "on_submit")

        assert invoice_helper.create_from_sales_invoice.called

    def test_call_document_generate(self,
                                    agent_response_mock,
                                    invoice_helper,
                                    document_generate,
                                    pdf_file_helper_mock,
                                    agent_invoice_helper_mock):
        sales_invoice = frappe.new_doc("Sales Invoice")
        seller = frappe.new_doc("Company")
        buyer = frappe.new_doc("Customer")
        invoice_helper.create_from_sales_invoice.return_value = Invoice(seller, buyer)
        self._setup_document_generate(document_generate)
        self._setup_pdf_file_helper(pdf_file_helper_mock)
        self._setup_agent_invoice_helper(agent_invoice_helper_mock)
        agent_response_mock.handle_response.return_value = Invoice(seller, buyer)

        on_submit(sales_invoice, "on_submit")

        assert document_generate.called

    def _setup_document_generate(self, document_generate):
        request = SzamlaAgentRequest(None, None, None)
        response = ""
        document_generate.return_value = {request, response}

    def _setup_pdf_file_helper(self, pdf_file_helper_mock):
        file = self._create_file()
        pdf_file_helper_mock.create_and_insert_from_agent_result.return_value = file

    def _setup_agent_invoice_helper(self, agent_invoice_helper_mock):
        invoice = frappe.new_doc("SzamlazzAgentConnectorInvoice")
        agent_invoice_helper_mock.create_and_insert_from_sales_invoice.return_value = invoice

    def _create_file(self):
        file = frappe.new_doc("File")
        file.save = Mock()
        return file
