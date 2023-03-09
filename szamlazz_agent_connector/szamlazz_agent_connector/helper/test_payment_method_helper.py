from unittest.mock import patch, Mock

import frappe
from frappe.tests.utils import FrappeTestCase
from szamlazz_agent_connector.szamlazz_agent_connector.helper.payment_method_helper import PaymentMethodHelper
from szamlazz_agent_connector.szamlazz_agent_connector.helper.payment_mode_helper import PaymentModeHelper
from szamlazz_agent_connector.szamlazz_agent_connector.model.constant.document_constant import DocumentConstant


@patch("szamlazz_agent_connector.szamlazz_agent_connector.helper.payment_method_helper.frappe")
class TestPaymentMethodHelper(FrappeTestCase):
    def test_return_cash_if_no_term(self, frappe_mock):
        frappe_mock.get_all.return_value = None

        result = PaymentMethodHelper.get_payment_method("")

        self.assertEqual(result, DocumentConstant.PAYMENT_METHOD_CASH)

    def test_return_payment_method_if_term(self, frappe_mock):
        PAYMENT_METHOD = DocumentConstant.PAYMENT_METHOD_PAYPAL
        self._setup_frappe_mock(frappe_mock)
        self._setup_payment_mode_helper(PAYMENT_METHOD)

        assert PaymentMethodHelper.get_payment_method("") == PAYMENT_METHOD

    def _setup_frappe_mock(self, frappe_mock):
        term = frappe.new_doc("Payment Terms Template Detail")
        frappe_mock.get_all.return_value = [term]
        frappe_mock.get_doc.return_value = term

    def _setup_payment_mode_helper(self, PAYMENT_METHOD):
        PaymentModeHelper.get_payment_mode = Mock()
        PaymentModeHelper.get_payment_mode.return_value = PAYMENT_METHOD

