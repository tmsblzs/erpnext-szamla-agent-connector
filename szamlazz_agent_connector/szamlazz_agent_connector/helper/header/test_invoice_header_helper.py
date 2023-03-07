import unittest
from unittest.mock import patch

import frappe
from frappe.tests.utils import FrappeTestCase
from szamlazz_agent_connector.szamlazz_agent_connector.helper.header.invoice_header_helper import InvoiceHeaderHelper
from szamlazz_agent_connector.szamlazz_agent_connector.model.header.invoice_header import InvoiceHeader


@patch("szamlazz_agent_connector.szamlazz_agent_connector.helper.header.invoice_header_helper.PaymentMethodHelper")
class TestInvoiceHeaderHelper(FrappeTestCase):
    def test_payment_method_is_set(self, payment_method_helper_mock):
        PAYMENT_METHOD = 'Készpénz'
        payment_method_helper_mock.get_payment_method.return_value = PAYMENT_METHOD
        header = InvoiceHeader()
        sales_invoice = frappe.new_doc("Sales Invoice")
        sales_invoice.fulfillment_date = None

        InvoiceHeaderHelper.fill_from_sales_invoice(header, sales_invoice)

        self.assertEqual(header.payment_method, PAYMENT_METHOD)

    def test_fulfillment_is_set(self, payment_method_helper_mock):
        FULFILLMENT_DATE = '2023-01-07'
        self._setup_payment_method_get_payment_method(payment_method_helper_mock)
        header = InvoiceHeader()
        sales_invoice = frappe.new_doc("Sales Invoice")
        sales_invoice.fulfillment_date = FULFILLMENT_DATE

        InvoiceHeaderHelper.fill_from_sales_invoice(header, sales_invoice)

        self.assertEqual(header.fulfillment, FULFILLMENT_DATE)


    def _setup_payment_method_get_payment_method(self, payment_method_helper_mock):
        payment_method_helper_mock.return_value = None
