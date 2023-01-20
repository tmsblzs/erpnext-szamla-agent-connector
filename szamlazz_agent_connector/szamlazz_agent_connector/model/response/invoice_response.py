
from szamlazz_agent_connector.szamlazz_agent_connector.model.constant.invoice_constant import InvoiceConstant
from szamlazz_agent_connector.szamlazz_agent_connector.model.constant.response_constant import ResponseConstant


class InvoiceResponse:

    @property
    def document_number(self):
        return self.invoice_number

    def __init__(self):
        self.headers = None
        self.invoice_number = None
        self.user_account_url = None
        self.asset_amount = None
        self.net_price = None
        self.gross_amount = None
        self.error_message = None
        self.error_code = None
        self.pdf_data = None
        self.success = False

    def is_error(self):
        if self.error_message or self.error_code:
            return True
        if self.invoice_number and self.has_invoice_notification_send_error():
            return False
        return False

    def has_invoice_notification_send_error(self):
        if self.error_code == InvoiceConstant.INVOICE_NOTIFICATION_SEND_FAILED:
            return True
        return False
