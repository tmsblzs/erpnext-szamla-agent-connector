import unittest
from unittest.mock import patch

import frappe
from frappe.tests.utils import FrappeTestCase
from szamlazz_agent_connector.szamlazz_agent_connector.helper.payment_mode_helper import PaymentModeHelper
from szamlazz_agent_connector.szamlazz_agent_connector.model.constant.document_constant import DocumentConstant


@patch("szamlazz_agent_connector.szamlazz_agent_connector.helper.payment_mode_helper.frappe")
class TestPaymentModeHelper(FrappeTestCase):
    def test_return_method_cash_as_default(self, frappe_mock):
        frappe_mock.get_all.return_value = None

        result = PaymentModeHelper.get_payment_mode("")

        assert result == DocumentConstant.PAYMENT_METHOD_CASH

    def test_return_agent_payment_method_type_if_exists(self, frappe_mock):
        AGENT_PAYMENT_METHOD_TYPE = 'test'
        agent_mode_of_payment = \
            self._create_agent_connector_mode_of_payments(payment_method_type=AGENT_PAYMENT_METHOD_TYPE)
        self._setup_frappe_mock(frappe_mock, agent_mode_of_payment)

        result = PaymentModeHelper.get_payment_mode("")

        assert result == AGENT_PAYMENT_METHOD_TYPE

    def test_get_all_called_once_with_correct_args(self, frappe_mock):
        MODE_OF_PAYMENT = 'Test mode of payment'
        self._setup_frappe_mock(frappe_mock)

        PaymentModeHelper.get_payment_mode(MODE_OF_PAYMENT)

        frappe_mock.get_all.assert_called_once_with(
            'SzamlazzAgentConnectorModeOfPayments',
            filters={'mode_of_payment_name': MODE_OF_PAYMENT}
        )

    def test_get_doc_called_once_with_correct_args(self, frappe_mock):
        AGENT_MODE_OF_PAYMENT = self._create_agent_connector_mode_of_payments()
        self._setup_frappe_mock(frappe_mock, AGENT_MODE_OF_PAYMENT)

        PaymentModeHelper.get_payment_mode("")

        frappe_mock.get_doc.assert_called_once_with(
            'SzamlazzAgentConnectorModeOfPayments',
            AGENT_MODE_OF_PAYMENT
        )

    def _create_agent_connector_mode_of_payments(self, payment_method_type=None):
        agent_mode_of_payment = frappe.new_doc('SzamlazzAgentConnectorModeOfPayments')
        agent_mode_of_payment.agent_payment_method_type = payment_method_type
        return agent_mode_of_payment

    def _setup_frappe_mock(self, frappe_mock, agent_mode_of_payment=None):
        if agent_mode_of_payment is None:
            agent_mode_of_payment = self._create_agent_connector_mode_of_payments()
        frappe_mock.get_all.return_value = [agent_mode_of_payment]
        frappe_mock.get_doc.return_value = agent_mode_of_payment
