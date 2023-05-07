from unittest.mock import patch, Mock

import frappe
from frappe.tests.utils import FrappeTestCase
from szamlazz_agent_connector.szamlazz_agent_connector.helper.payment_method_helper import PaymentMethodHelper
from szamlazz_agent_connector.szamlazz_agent_connector.helper.payment_mode_helper import PaymentModeHelper
from szamlazz_agent_connector.szamlazz_agent_connector.model.constant.document_constant import DocumentConstant


@patch("szamlazz_agent_connector.szamlazz_agent_connector.helper.payment_method_helper.frappe")
class TestPaymentMethodHelper(FrappeTestCase):
    def setUp(self):
        self.get_payment_mode = PaymentModeHelper.get_payment_mode

    def tearDown(self):
        PaymentModeHelper.get_payment_mode = self.get_payment_mode

    def test_return_cash_if_no_term(self, frappe_mock):
        frappe_mock.get_all.return_value = None

        result = PaymentMethodHelper.get_payment_method("")

        self.assertEqual(result, DocumentConstant.PAYMENT_METHOD_CASH)

    def test_return_payment_method_if_term(self, frappe_mock):
        PAYMENT_METHOD = DocumentConstant.PAYMENT_METHOD_PAYPAL
        self._setup_frappe_mock(frappe_mock)
        self._setup_payment_mode_helper(PAYMENT_METHOD)

        assert PaymentMethodHelper.get_payment_method("") == PAYMENT_METHOD

    def test_frappe_get_all_called_with_correct_args(self, frappe_mock):
        TEMPLATE_NAME = 'Test'
        self._setup_frappe_mock(frappe_mock)
        self._setup_payment_mode_helper()

        PaymentMethodHelper.get_payment_method(TEMPLATE_NAME)

        frappe_mock.get_all.assert_called_once_with("Payment Terms Template Detail",
                               filters={'payment_term': TEMPLATE_NAME},
                               fields=['name'])

    def test_frappe_get_doc_called_with_correct_args(self, frappe_mock):
        TERM_NAME = 'Test name'
        term = self._create_payment_term_template_detail(term_name=TERM_NAME)
        self._setup_frappe_mock(frappe_mock, term)
        self._setup_payment_mode_helper()

        PaymentMethodHelper.get_payment_method("")

        frappe_mock.get_doc.assert_called_once_with(
            "Payment Terms Template Detail", TERM_NAME)

    def test_get_payment_mode_called_with_correct_args(self, frappe_mock):
        TERM_MODE_OF_PAYMENT = 'CASH'
        term = self._create_payment_term_template_detail(mode_of_payment=TERM_MODE_OF_PAYMENT)
        self._setup_frappe_mock(frappe_mock, term)
        self._setup_payment_mode_helper()

        PaymentMethodHelper.get_payment_method("")

        PaymentModeHelper.get_payment_mode\
            .assert_called_once_with(TERM_MODE_OF_PAYMENT)

    def _create_payment_term_template_detail(self, term_name=None, mode_of_payment=None):
        term = frappe.new_doc("Payment Terms Template Detail")
        term.name = term_name
        term.mode_of_payment = mode_of_payment
        return term

    def _setup_frappe_mock(self, frappe_mock, term=None):
        if term is None:
            term = self._create_payment_term_template_detail()
        frappe_mock.get_all.return_value = [term]
        frappe_mock.get_doc.return_value = term

    def _setup_payment_mode_helper(self, payment_method=None):
        PaymentModeHelper.get_payment_mode = Mock()
        PaymentModeHelper.get_payment_mode.return_value = payment_method
