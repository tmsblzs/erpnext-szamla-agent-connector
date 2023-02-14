import frappe
from szamlazz_agent_connector.szamlazz_agent_connector.events.sales_invoice import on_submit

from frappe.tests.utils import FrappeTestCase
from unittest.mock import patch
from szamlazz_agent_connector.szamlazz_agent_connector.model.document.invoice.invoice import Invoice


class TestSalesInvoice(FrappeTestCase):

    @patch("szamlazz_agent_connector.szamlazz_agent_connector.helper.document.invoice_helper.InvoiceHelper")
    def test_call_create_from_sales_invoice(self, invoice_helper):
        sales_invoice = frappe.new_doc("Sales Invoice")
        seller = frappe.new_doc("Company")
        buyer = frappe.new_doc("Customer")
        invoice_helper.create_from_sales_invoice.return_value = Invoice(seller, buyer)

        on_submit(sales_invoice, "on_submit")

        assert invoice_helper.create_from_sales_invoice.called

