from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.constant.document_constant import DocumentConstant
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.constant.invoice_constant import InvoiceConstant


class InvoiceHeaderHelper:

    @staticmethod
    def fill_from_sales_invoice(header, sales_invoice):
        header.payment_method = DocumentConstant.PAYMENT_METHOD_TRANSFER
        header.fulfillment = sales_invoice.fulfillment_date
        header.payment_due = sales_invoice.due_date
        header.prefix = ''
        header.preview_pdf = False
        header.invoice_template = InvoiceConstant.INVOICE_TEMPLATE_DEFAULT
        return header
