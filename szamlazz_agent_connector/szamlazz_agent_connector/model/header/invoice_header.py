from szamlazz_agent_connector.szamlazz_agent_connector.model.constant.document_constant import DocumentConstant
from szamlazz_agent_connector.szamlazz_agent_connector.model.constant.invoice_constant import InvoiceConstant
from szamlazz_agent_connector.szamlazz_agent_connector.model.document.document import Document
from szamlazz_agent_connector.szamlazz_agent_connector.model.header.document_header import DocumentHeader
from szamlazz_agent_connector.szamlazz_agent_connector.model.szamla_agent_util import SzamlaAgentUtil


class InvoiceHeader(DocumentHeader):
    def __init__(self, invoice_type=InvoiceConstant.INVOICE_TYPE_P_INVOICE):
        super().__init__()
        self.invoice_number = ""
        self.invoice_type = 0
        self.issue_date = ""
        self.payment_method = 0
        self.currency = ""
        self.language = ""
        self.fulfillment = ""
        self.payment_due = ""
        self.prefix = ""
        self.extra_logo = ""
        self.correction_to_pay = ""
        self.correctived_number = ""
        self.comment = ""
        self.exchange_bank = ""
        self.exchange_rate = 0
        self.order_number = ""
        self.proforma_number = ""
        self.paid = False
        self.profit_vat = False
        self.invoice_template = InvoiceConstant.INVOICE_TEMPLATE_DEFAULT
        self.preview_pdf = False

        if invoice_type:
            self._set_default(invoice_type)

    def is_e_invoice(self):
        return self.invoice_type == InvoiceConstant.INVOICE_TYPE_E_INVOICE

    def _set_default(self, invoice_type):
        self.invoice = True
        self.invoice_type = invoice_type
        self.issue_date = SzamlaAgentUtil.get_today_str()
        self.payment_method = DocumentConstant.PAYMENT_METHOD_TRANSFER
        self.currency = Document.get_default_currency()
        self.language = Document.get_default_language()
        self.fulfillment = SzamlaAgentUtil.get_today_str()
        self.payment_due = SzamlaAgentUtil.add_days_to_date(SzamlaAgentUtil.DEFAULT_ADDED_DAYS)

