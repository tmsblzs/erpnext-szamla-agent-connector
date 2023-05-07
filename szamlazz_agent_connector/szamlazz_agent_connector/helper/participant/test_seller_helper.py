from unittest.mock import patch

import frappe
from frappe.tests.utils import FrappeTestCase
from szamlazz_agent_connector.szamlazz_agent_connector.helper.participant.seller_helper import SellerHelper


@patch("szamlazz_agent_connector.szamlazz_agent_connector.helper.participant.seller_helper.frappe")
@patch("szamlazz_agent_connector.szamlazz_agent_connector.helper.participant.seller_helper.AccountHelper")
class TestSellerHelper(FrappeTestCase):
    BANK = "OTP BANK NYRT"
    BANK_ACCOUNT = "11111111-22222222"

    def test_call_get_account_or_default(self, account_helper_mock, frappe_mock):
        company = TestSellerHelper._setup_company(frappe_mock)
        sales_invoice = TestSellerHelper._setup_sales_invoice(company)

        SellerHelper.get_from_sales_invoice(sales_invoice)

        assert account_helper_mock.get_account_or_default.called

    def test_return_seller(self, account_helper_mock, frappe_mock):
        company = TestSellerHelper._setup_company(frappe_mock)
        sales_invoice = TestSellerHelper._setup_sales_invoice(company)
        TestSellerHelper._setup_account_helper(account_helper_mock)

        result = SellerHelper.get_from_sales_invoice(sales_invoice)

        self.assertEqual(result.bank, TestSellerHelper.BANK)
        self.assertEqual(result.bank_account, TestSellerHelper.BANK_ACCOUNT)

    @staticmethod
    def _setup_account_helper(account_helper_mock):
        account = {
            'bank': TestSellerHelper.BANK,
            'account_no': TestSellerHelper.BANK_ACCOUNT}
        account_helper_mock.get_account_or_default.return_value = account
        return account

    @staticmethod
    def _setup_sales_invoice(company):
        sales_invoice = frappe.new_doc("Sales Invoice")
        sales_invoice.company = company
        return sales_invoice

    @staticmethod
    def _setup_company(frappe_mock):
        company = frappe.new_doc("Company")
        company.name = "Test 1"
        frappe_mock.get_doc('Company').return_value = company
        return company

