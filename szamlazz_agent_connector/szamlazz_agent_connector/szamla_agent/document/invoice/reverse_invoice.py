from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.constant.invoice_constant import InvoiceConstant
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.document.invoice.invoice import Invoice
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.header.reverse_invoice_header import \
    ReverseInvoiceHeader


class ReverseInvoice(Invoice):
    def __init__(self, invoice_type=InvoiceConstant.INVOICE_TYPE_P_INVOICE):
        super().__init__()
        if invoice_type:
            self.header = ReverseInvoiceHeader(invoice_type)
