import unittest
from unittest.mock import patch

import frappe
from frappe.tests.utils import FrappeTestCase
from szamlazz_agent_connector.szamlazz_agent_connector.helper.participant.tax_helper import TaxHelper


class MyTestCase(FrappeTestCase):
    def test_no_tax_rate_if_no_stock_item_tax(self):
        stock_item = self._create_stock_item()
        TAX_CATEGORY = "Test Tax Category"

        result = TaxHelper.get_tax_rate_from_stock_item_by_tax_category(stock_item, TAX_CATEGORY)

        assert result == 0

    @patch("szamlazz_agent_connector.szamlazz_agent_connector.helper.participant.tax_helper.frappe")
    def test_call_frappe_get_item_tax_template(self, frappe_mock):
        TAX_CATEGORY = "Test Tax Category"
        ITEM_TAX_TEMPLATE = "Test Item Tax Template"
        stock_item = self._create_stock_item(TAX_CATEGORY, ITEM_TAX_TEMPLATE)
        tax_template = self._create_item_tax_template()
        frappe_mock.get_doc.return_value = tax_template

        TaxHelper.get_tax_rate_from_stock_item_by_tax_category(stock_item, TAX_CATEGORY)

        frappe_mock.get_doc.assert_called_once_with("Item Tax Template", ITEM_TAX_TEMPLATE)

    @patch("szamlazz_agent_connector.szamlazz_agent_connector.helper.participant.tax_helper.frappe")
    def test_return_tax_template_detail_tax_rate(self, frappe_mock):
        TAX_CATEGORY = "Test Tax Category"
        ITEM_TAX_TEMPLATE = "Test Item Tax Template"
        TAX_RATE = 25
        stock_item = self._create_stock_item(TAX_CATEGORY, ITEM_TAX_TEMPLATE)
        tax_template = self._create_item_tax_template(tax_rate=TAX_RATE)
        frappe_mock.get_doc.return_value = tax_template

        result = TaxHelper.get_tax_rate_from_stock_item_by_tax_category(stock_item, TAX_CATEGORY)

        assert result == TAX_RATE

    def _create_stock_item(self, tax_category=None, item_tax_template=None):
        stock_item = frappe.new_doc("Item")
        item_tax = self._create_item_tax(
            tax_category=tax_category,
            item_tax_template=item_tax_template)
        stock_item.taxes = [item_tax]
        return stock_item

    def _create_item_tax(self, tax_category=None, item_tax_template=None):
        item_tax = frappe.new_doc("Item Tax")
        item_tax.tax_category = tax_category
        item_tax.item_tax_template = item_tax_template
        return item_tax

    def _create_item_tax_template(self, tax_rate=None):
        item_tax_template = frappe.new_doc("Item Tax Template")
        tax_detail = self._create_item_tax_template_detail(tax_rate=tax_rate)
        item_tax_template.taxes = [tax_detail]
        return item_tax_template

    def _create_item_tax_template_detail(self, tax_rate=None):
        tax_detail = frappe.new_doc("Item Tax Template Detail")
        tax_detail.tax_rate = tax_rate
        return tax_detail



