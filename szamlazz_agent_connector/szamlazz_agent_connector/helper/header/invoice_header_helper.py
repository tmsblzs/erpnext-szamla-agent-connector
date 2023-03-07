from szamlazz_agent_connector.szamlazz_agent_connector.helper.address.shipping_address_helper import \
    ShippingAddressHelper
from szamlazz_agent_connector.szamlazz_agent_connector.helper.payment_method_helper import PaymentMethodHelper
from szamlazz_agent_connector.szamlazz_agent_connector.model.constant.invoice_constant import InvoiceConstant


class InvoiceHeaderHelper:
    @staticmethod
    def fill_from_sales_invoice(header, sales_invoice):
        header.payment_method = PaymentMethodHelper.get_payment_method(sales_invoice.payment_terms_template)
        header.fulfillment = sales_invoice.fulfillment_date
        header.payment_due = sales_invoice.due_date
        header.prefix = ''
        header.preview_pdf = False
        header.invoice_template = InvoiceConstant.INVOICE_TEMPLATE_DEFAULT
        shipping_address = sales_invoice.shipping_address if sales_invoice.shipping_address is not None else None
        if shipping_address:
            header.comment = ShippingAddressHelper.format(shipping_address)
        return header

