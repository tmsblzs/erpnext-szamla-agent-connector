from szamlazz_agent_connector.szamlazz_agent_connector.helper.agent.agent_invoice_helper import AgentInvoiceHelper
from szamlazz_agent_connector.szamlazz_agent_connector.helper.header.reverse_invoice_header_helper import \
    ReverseInvoiceHeaderHelper
from szamlazz_agent_connector.szamlazz_agent_connector.model.document.invoice.reverse_invoice import \
    ReverseInvoice


class ReverseInvoiceHelper:
    @staticmethod
    def create_from_sales_invoice(sales_invoice):
        agent_invoice = AgentInvoiceHelper.get_by_own_invoice_number(sales_invoice.name)
        reverse_invoice = ReverseInvoice()
        ReverseInvoiceHeaderHelper.fill_from_sales_invoice(reverse_invoice.header, agent_invoice)
        return reverse_invoice
