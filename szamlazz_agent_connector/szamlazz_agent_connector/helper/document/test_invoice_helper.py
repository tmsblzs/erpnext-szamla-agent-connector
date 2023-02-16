from unittest.mock import patch

import frappe
from frappe.tests.utils import FrappeTestCase
from szamlazz_agent_connector.szamlazz_agent_connector.helper.document.invoice_helper import InvoiceHelper
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.buyer import Buyer
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.seller import Seller


@patch("szamlazz_agent_connector.szamlazz_agent_connector.helper.document.invoice_helper.SalesItemsHelper")
@patch("szamlazz_agent_connector.szamlazz_agent_connector.helper.document.invoice_helper.InvoiceHeaderHelper")
@patch("szamlazz_agent_connector.szamlazz_agent_connector.helper.document.invoice_helper.SellerHelper")
@patch("szamlazz_agent_connector.szamlazz_agent_connector.helper.document.invoice_helper.BuyerHelper")
class TestInvoiceHelper(FrappeTestCase):

    def test_call_get_from_sales_invoice(
            self,
            buyer_helper,
            seller_helper,
            invoice_header_helper,
            sales_items_helper):
        seller_helper.get_from_sales_invoice.return_value = Seller
        buyer_helper.get_buyer_from_sales_invoice.return_value = Buyer
        sales_invoice = frappe.new_doc("Sales Invoice")

        InvoiceHelper.create_from_sales_invoice(sales_invoice)

        assert seller_helper.get_from_sales_invoice.called

    def test_call_get_buyer_from_sales_invoice(
            self,
            buyer_helper,
            seller_helper,
            invoice_header_helper,
            sales_items_helper):
        seller_helper.get_from_sales_invoice.return_value = Seller
        buyer_helper.get_buyer_from_sales_invoice.return_value = Buyer
        sales_invoice = frappe.new_doc("Sales Invoice")

        InvoiceHelper.create_from_sales_invoice(sales_invoice)

        assert buyer_helper.get_buyer_from_sales_invoice.called

    def test_call_fill_form_sales_invoice(
            self,
            buyer_helper,
            seller_helper,
            invoice_header_helper,
            sales_items_helper):
        seller_helper.get_from_sales_invoice.return_value = Seller
        buyer_helper.get_buyer_from_sales_invoice.return_value = Buyer
        sales_invoice = frappe.new_doc("Sales Invoice")

        InvoiceHelper.create_from_sales_invoice(sales_invoice)

        assert invoice_header_helper.fill_from_sales_invoice.called

    def test_call_add_items_to_invoice(
            self,
            buyer_helper,
            seller_helper,
            invoice_header_helper,
            sales_items_helper):
        seller_helper.get_from_sales_invoice.return_value = Seller
        buyer_helper.get_buyer_from_sales_invoice.return_value = Buyer
        sales_invoice = frappe.new_doc("Sales Invoice")

        InvoiceHelper.create_from_sales_invoice(sales_invoice)

        assert sales_items_helper.add_items_to_invoice.called
