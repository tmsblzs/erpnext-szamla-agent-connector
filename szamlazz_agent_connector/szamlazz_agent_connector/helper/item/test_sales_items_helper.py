import unittest
from unittest.mock import patch

import frappe
from frappe.tests.utils import FrappeTestCase
from szamlazz_agent_connector.szamlazz_agent_connector.helper.item.sales_items_helper import SalesItemsHelper
from szamlazz_agent_connector.szamlazz_agent_connector.model.document.invoice.invoice import Invoice


@patch("szamlazz_agent_connector.szamlazz_agent_connector.helper.item.sales_items_helper.SalesItemHelper")
class TestSalesItemsHelper(FrappeTestCase):
    def test_something(self, sales_item_mock):
        tax_category = 'Tax Category'
        invoice = self._create_invoice()
        sales_item = self._create_sales_item()
        sales_item_mock.get_item_from_sales_invoice_item.return_value = sales_item

        SalesItemsHelper.add_items_to_invoice(invoice, [sales_item], tax_category)

        sales_item_mock.get_item_from_sales_invoice_item\
            .assert_called_with(sales_item, tax_category)

    def test_add_item_to_invoice_item(self, sales_item_mock):
        tax_category = 'Tax Category'
        invoice = self._create_invoice()
        sales_item = self._create_sales_item()
        sales_item_mock.get_item_from_sales_invoice_item.return_value = sales_item

        SalesItemsHelper.add_items_to_invoice(invoice, [sales_item], tax_category)

        self.assertIn(sales_item, invoice.items)

    def _create_invoice(self):
        return Invoice(None, None)

    def _create_sales_item(self):
        sales_item = frappe.new_doc('Item')
        return sales_item
