from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.constant.invoice_constant import InvoiceConstant


class ReverseInvoiceHeaderHelper:
    @staticmethod
    def fill_from_sales_invoice(header, agent_invoice):
        header.invoice_number = agent_invoice.szamlazz_invoice_number.upper()
        header.invoice_template = InvoiceConstant.INVOICE_TEMPLATE_DEFAULT
        return header
