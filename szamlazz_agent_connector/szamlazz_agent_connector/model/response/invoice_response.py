from szamlazz_agent_connector.szamlazz_agent_connector.model.constant.agent_constant import AgentConstant
from szamlazz_agent_connector.szamlazz_agent_connector.model.constant.invoice_constant import InvoiceConstant
from szamlazz_agent_connector.szamlazz_agent_connector.model.constant.response_constant import ResponseConstant
from szamlazz_agent_connector.szamlazz_agent_connector.model.szamla_agent_util import SzamlaAgentUtil


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
        self.xml_data = None

    def to_pdf(self):
        return self.pdf_data

    def is_error(self):
        if self.error_message or self.error_code:
            return True
        if self.invoice_number and self.has_invoice_notification_send_error():
            return False
        return False

    def is_success(self):
        return not self.is_failed()

    def is_failed(self):
        return self.is_error()

    def has_invoice_notification_send_error(self):
        if self.error_code == InvoiceConstant.INVOICE_NOTIFICATION_SEND_FAILED:
            return True
        return False

    def get_pdf_file_name(self, with_path=True):
        if with_path:
            filename = InvoiceResponse.get_pdf_file_abs_path(f'{self.invoice_number}')
        else:
            filename = f"{self.invoice_number}"
        return f"{filename}.pdf"

    @staticmethod
    def get_pdf_file_abs_path(pdf_file_name):
        return SzamlaAgentUtil.get_abs_path(AgentConstant.PDF_FILE_SAVE_PATH, pdf_file_name)