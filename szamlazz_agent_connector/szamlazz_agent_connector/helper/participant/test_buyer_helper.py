from unittest.mock import patch

import frappe
from frappe.tests.utils import FrappeTestCase
from szamlazz_agent_connector.szamlazz_agent_connector.helper.participant.buyer_helper import BuyerHelper
from szamlazz_agent_connector.szamlazz_agent_connector.model.constant.tax_payer_constant import TaxPayerConstant


@patch("szamlazz_agent_connector.szamlazz_agent_connector.helper.participant.buyer_helper.frappe")
class TestBuyerHelper(FrappeTestCase):
    CUSTOMER_NAME = "TEST 1"
    ADDRESS_PIN_CODE = "2222"
    ADDRESS_CITY = "TEST CITY"
    ADDRESS_LINE1 = "TEST ADDRESS LINE 1"
    CUSTOMER_TAX_ID = "12345678-1-12"

    def test_customer_name_is_set(self, frappe_mock):
        frappe_mock.get_doc.side_effect = self._get_doc_side_effect
        sales_invoice = TestBuyerHelper._setup_sales_invoice()

        result = BuyerHelper.get_buyer_from_sales_invoice(sales_invoice)

        self.assertEqual(result.name, TestBuyerHelper.CUSTOMER_NAME)

    def test_address_pincode_is_set(self, frappe_mock):
        frappe_mock.get_doc.side_effect = self._get_doc_side_effect
        sales_invoice = TestBuyerHelper._setup_sales_invoice()

        result = BuyerHelper.get_buyer_from_sales_invoice(sales_invoice)

        self.assertEqual(result.zip_code, TestBuyerHelper.ADDRESS_PIN_CODE)

    def test_address_city_is_set(self, frappe_mock):
        frappe_mock.get_doc.side_effect = self._get_doc_side_effect
        sales_invoice = TestBuyerHelper._setup_sales_invoice()

        result = BuyerHelper.get_buyer_from_sales_invoice(sales_invoice)

        self.assertEqual(result.city, TestBuyerHelper.ADDRESS_CITY)

    def test_address_line1_is_set(self, frappe_mock):
        frappe_mock.get_doc.side_effect = self._get_doc_side_effect
        sales_invoice = TestBuyerHelper._setup_sales_invoice()

        result = BuyerHelper.get_buyer_from_sales_invoice(sales_invoice)

        self.assertEqual(result.address, TestBuyerHelper.ADDRESS_LINE1)

    def test_tax_number_is_set(self, frappe_mock):
        frappe_mock.get_doc.side_effect = self._get_doc_side_effect
        sales_invoice = TestBuyerHelper._setup_sales_invoice()

        result = BuyerHelper.get_buyer_from_sales_invoice(sales_invoice)

        self.assertEqual(result.tax_number, TestBuyerHelper.CUSTOMER_TAX_ID)

    def test_tax_payer_is_set(self, frappe_mock):
        frappe_mock.get_doc.side_effect = self._get_doc_side_effect
        sales_invoice = TestBuyerHelper._setup_sales_invoice()

        result = BuyerHelper.get_buyer_from_sales_invoice(sales_invoice)

        self.assertEqual(result.tax_payer, TaxPayerConstant.TAXPAYER_HAS_TAXNUMBER)

    @staticmethod
    def _setup_sales_invoice():
        sales_invoice = frappe.new_doc("Sales Invoice")
        return sales_invoice

    @staticmethod
    def _get_doc_side_effect(*args, **kwargs):
        if args[0] == 'Customer':
            customer = frappe.new_doc("Customer")
            customer.customer_name = TestBuyerHelper.CUSTOMER_NAME
            customer.tax_id = TestBuyerHelper.CUSTOMER_TAX_ID
            return customer
        elif args[0] == 'Address':
            address = frappe.new_doc("Address")
            address.pincode = TestBuyerHelper.ADDRESS_PIN_CODE
            address.city = TestBuyerHelper.ADDRESS_CITY
            address.address_line1 = TestBuyerHelper.ADDRESS_LINE1
            return address


