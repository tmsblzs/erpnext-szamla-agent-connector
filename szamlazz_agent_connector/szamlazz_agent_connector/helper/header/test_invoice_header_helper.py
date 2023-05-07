import unittest
from unittest.mock import patch

import frappe
from frappe.tests.utils import FrappeTestCase
from szamlazz_agent_connector.szamlazz_agent_connector.helper.address.shipping_address_helper import \
    ShippingAddressHelper
from szamlazz_agent_connector.szamlazz_agent_connector.helper.header.invoice_header_helper import InvoiceHeaderHelper
from szamlazz_agent_connector.szamlazz_agent_connector.model.constant.invoice_constant import InvoiceConstant
from szamlazz_agent_connector.szamlazz_agent_connector.model.header.invoice_header import InvoiceHeader


@patch("szamlazz_agent_connector.szamlazz_agent_connector.helper.header.invoice_header_helper.PaymentMethodHelper")
class TestInvoiceHeaderHelper(FrappeTestCase):
    def test_payment_method_is_set(self, payment_method_helper_mock):
        PAYMENT_METHOD = 'Készpénz'
        payment_method_helper_mock.get_payment_method.return_value = PAYMENT_METHOD
        header = self._create_invoice_header()
        sales_invoice = self._create_sales_invoice()

        InvoiceHeaderHelper.fill_from_sales_invoice(header, sales_invoice)

        self.assertEqual(header.payment_method, PAYMENT_METHOD)

    def test_fulfillment_is_set(self, payment_method_helper_mock):
        FULFILLMENT_DATE = '2023-01-07'
        self._setup_payment_method_get_payment_method(payment_method_helper_mock)
        header = self._create_invoice_header()
        sales_invoice = self._create_sales_invoice(fulfillment_date=FULFILLMENT_DATE)

        InvoiceHeaderHelper.fill_from_sales_invoice(header, sales_invoice)

        self.assertEqual(header.fulfillment, FULFILLMENT_DATE)

    def test_payment_date_is_set(self, payment_method_helper_mock):
        DUE_DATE = '2023-01-11'
        self._setup_payment_method_get_payment_method(payment_method_helper_mock)
        header = self._create_invoice_header()
        sales_invoice = self._create_sales_invoice(due_date=DUE_DATE)

        InvoiceHeaderHelper.fill_from_sales_invoice(header, sales_invoice)

        self.assertEqual(header.payment_due, DUE_DATE)

    def test_prefix_set_to_empty(self, payment_method_helper_mock):
        self._setup_payment_method_get_payment_method(payment_method_helper_mock)
        header = self._create_invoice_header()
        sales_invoice = self._create_sales_invoice()

        InvoiceHeaderHelper.fill_from_sales_invoice(header, sales_invoice)

        self.assertEqual(header.prefix, '')

    def test_preview_pdf_is_false(self, payment_method_helper_mock):
        self._setup_payment_method_get_payment_method(payment_method_helper_mock)
        header = self._create_invoice_header()
        sales_invoice = self._create_sales_invoice()

        InvoiceHeaderHelper.fill_from_sales_invoice(header, sales_invoice)

        self.assertEqual(header.preview_pdf, False)

    def test_invoice_template_is_default(self, payment_method_helper_mock):
        self._setup_payment_method_get_payment_method(payment_method_helper_mock)
        header = self._create_invoice_header()
        sales_invoice = self._create_sales_invoice()

        InvoiceHeaderHelper.fill_from_sales_invoice(header, sales_invoice)

        self.assertEqual(header.invoice_template, InvoiceConstant.INVOICE_TEMPLATE_DEFAULT)

    def test_comment_is_not_set_if_shipping_address_is_None(self, payment_method_helper_mock):
        SHIPPING_ADDRESS = None
        self._setup_payment_method_get_payment_method(payment_method_helper_mock)
        header = self._create_invoice_header()
        sales_invoice = self._create_sales_invoice(shipping_address=SHIPPING_ADDRESS)

        InvoiceHeaderHelper.fill_from_sales_invoice(header, sales_invoice)

        self.assertEqual(header.comment, '')

    def test_comment_is_set_if_shipping_address_is_not_None(self, payment_method_helper_mock):
        SHIPPING_ADDRESS = 'Test Address'
        self._setup_payment_method_get_payment_method(payment_method_helper_mock)
        header = self._create_invoice_header()
        sales_invoice = self._create_sales_invoice(shipping_address=SHIPPING_ADDRESS)

        InvoiceHeaderHelper.fill_from_sales_invoice(header, sales_invoice)

        self.assertEqual(header.comment,
                         ShippingAddressHelper.format(SHIPPING_ADDRESS))

    def _create_invoice_header(self):
        return InvoiceHeader()

    def _create_sales_invoice(self,
                              fulfillment_date=None,
                              due_date=None,
                              shipping_address=None):
        sales_invoice = frappe.new_doc("Sales Invoice")
        sales_invoice.fulfillment_date = fulfillment_date
        sales_invoice.due_date = due_date
        sales_invoice.shipping_address = shipping_address
        return sales_invoice

    def _setup_payment_method_get_payment_method(self, payment_method_helper_mock):
        payment_method_helper_mock.return_value = None
