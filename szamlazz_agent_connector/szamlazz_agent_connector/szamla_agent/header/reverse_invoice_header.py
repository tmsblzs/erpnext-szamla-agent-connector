from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.header.invoice_header import InvoiceHeader


class ReverseInvoiceHeader(InvoiceHeader):

    def __init__(self, invoice_type):
        super().__init__(invoice_type)
        self.reverse_invoice = True
        self.issue_date = None
        self.fulfillment = None
