import unittest
from unittest.mock import patch, Mock

import frappe
from frappe.tests.utils import FrappeTestCase
from szamlazz_agent_connector.szamlazz_agent_connector.helper.item.sales_item_helper import SalesItemHelper
from szamlazz_agent_connector.szamlazz_agent_connector.helper.participant.tax_helper import TaxHelper
from szamlazz_agent_connector.szamlazz_agent_connector.mapper.item.invoice_item_mapper import InvoiceItemMapper
from szamlazz_agent_connector.szamlazz_agent_connector.model.item.invoice_item import InvoiceItem


class TestSalesItemHelper(FrappeTestCase):
    def setUp(self):
        self._from_sales_invoice_item = InvoiceItemMapper.from_sales_invoice_item
        self._get_tax_rate_from_stock_item_by_tax_category = TaxHelper.get_tax_rate_from_stock_item_by_tax_category

    def tearDown(self):
        InvoiceItemMapper.from_sales_invoice_item = self._from_sales_invoice_item
        TaxHelper.get_tax_rate_from_stock_item_by_tax_category = self._get_tax_rate_from_stock_item_by_tax_category

    @patch("szamlazz_agent_connector.szamlazz_agent_connector.helper.item.sales_item_helper.frappe")
    def test_call_frappe_get_doc(self, frappe_mock):
        ITEM_CODE = "Test Item Code"
        sales_invoice_item = self._create_sales_invoice_item(item_code=ITEM_CODE)
        self._setup_tax_helper_get_tax_rate()

        SalesItemHelper\
            .get_item_from_sales_invoice_item(sales_invoice_item, "Test Category")

        frappe_mock.get_doc \
            .assert_called_once_with("Item", ITEM_CODE)

    @patch("szamlazz_agent_connector.szamlazz_agent_connector.helper.item.sales_item_helper.frappe")
    def test_call_tax_helper(self, frappe_mock):
        sales_invoice_item = self._create_sales_invoice_item()
        TAX_CATEGORY = "Test Tax Category"
        stock_item = frappe.new_doc("Item")
        frappe_mock.get_doc.return_value = stock_item
        self._setup_tax_helper_get_tax_rate()

        SalesItemHelper.get_item_from_sales_invoice_item(sales_invoice_item, TAX_CATEGORY)

        TaxHelper \
            .get_tax_rate_from_stock_item_by_tax_category \
            .assert_called_once_with(stock_item, TAX_CATEGORY)

    @patch("szamlazz_agent_connector.szamlazz_agent_connector.helper.item.sales_item_helper.frappe")
    def test_call_from_sales_invoice_item(self, frappe_mock):
        TAX_RATE = 27
        self._setup_tax_helper_get_tax_rate(tax_rate=TAX_RATE)
        sales_invoice_item = self._create_sales_invoice_item()
        self._setup_invoice_item_mapper()

        SalesItemHelper.get_item_from_sales_invoice_item(sales_invoice_item, "Test Tax Category")

        InvoiceItemMapper.from_sales_invoice_item \
            .assert_called_once_with(sales_invoice_item, TAX_RATE)

    def _setup_invoice_item_mapper(self):
        InvoiceItemMapper.from_sales_invoice_item = Mock()
        InvoiceItemMapper.from_sales_invoice_item.return_value = InvoiceItem("Test Item", 2)

    def _create_sales_invoice_item(self, item_code=None, net_amount=None):
        sales_invoice_item = frappe.new_doc("Sales Invoice Item")
        sales_invoice_item.item_code = item_code
        sales_invoice_item.net_amount = net_amount if net_amount is not None else 10
        return sales_invoice_item

    def _setup_tax_helper_get_tax_rate(self, tax_rate=5):
        TaxHelper.get_tax_rate_from_stock_item_by_tax_category = Mock()
        TaxHelper.get_tax_rate_from_stock_item_by_tax_category.return_value = tax_rate



