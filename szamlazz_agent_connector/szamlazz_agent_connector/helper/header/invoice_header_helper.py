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
            shipping_address = shipping_address.replace('\n', '')
            shipping_address = shipping_address.replace('<br>', '\n')
            header.comment = f"Szállítási cím: \n{shipping_address}\n"
        return header

