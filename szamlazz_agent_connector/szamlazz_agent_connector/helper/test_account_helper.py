from unittest.mock import patch

import frappe
from frappe.tests.utils import FrappeTestCase
from szamlazz_agent_connector.szamlazz_agent_connector.helper.account_helper import AccountHelper


@patch("szamlazz_agent_connector.szamlazz_agent_connector.helper.account_helper.frappe")
class TestAccountHelper(FrappeTestCase):
    def test_no_bank_account_returns_empty(self, frappe_mock):
        frappe_mock.get_all.return_value = None
        company = frappe.new_doc("Company")

        result = AccountHelper.get_account_or_default(company)

        self.assertEqual(result['bank'], "")
        self.assertEqual(result['account_no'], "")

    def test_no_bank_account_exists_returns_empty(self, frappe_mock):
        bank_account = frappe.new_doc("Bank Account")
        frappe_mock.get_all.return_value = [bank_account]
        frappe_mock.get_doc.return_value = None

        company = frappe.new_doc("Company")

        result = AccountHelper.get_account_or_default(company)

        self.assertEqual(result['bank'], "")
        self.assertEqual(result['account_no'], "")

    BANK = "OTP BANK NYRT"
    BANK_ACCOUNT_NO = "11111111-22222222"

    def test_bank_account_exists_returns_data(self, frappe_mock):
        bank_account = frappe.new_doc("Bank Account")
        bank_account.bank = TestAccountHelper.BANK
        bank_account.bank_account_no = TestAccountHelper.BANK_ACCOUNT_NO
        frappe_mock.get_all.return_value = [bank_account]
        frappe_mock.get_doc.return_value = bank_account

        company = frappe.new_doc("Company")

        result = AccountHelper.get_account_or_default(company)

        self.assertEqual(result['bank'], TestAccountHelper.BANK)
        self.assertEqual(result['account_no'], TestAccountHelper.BANK_ACCOUNT_NO)


