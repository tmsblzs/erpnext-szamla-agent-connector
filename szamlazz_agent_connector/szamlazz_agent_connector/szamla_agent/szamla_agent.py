import hashlib
import logging


# from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.document.invoice.invoice import Invoice
# from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.exception.szamla_agent_exception import \
#     SzamlaAgentException
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.constant.agent_constant import AgentConstant
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.response.szamla_agent_response import \
     SzamlaAgentResponse
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.szamla_agent_request import \
     SzamlaAgentRequest
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.szamla_agent_setting import SzamlaAgentSetting
# from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.szamla_agent_util import SzamlaAgentUtil
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.szamla_agent_util import SzamlaAgentUtil


class SzamlaAgent:
    logLevel = logging.NOTSET
    logEmail = ''

    callMethod  = SzamlaAgentRequest.CALL_METHOD_CURL
    certificationFileName = AgentConstant.CERTIFICATION_FILENAME
    cookieFileName = AgentConstant.COOKIE_FILENAME

    # @property
    # def setting(self):
    #     return self.__setting
    #
    # @setting.setter
    # def setting(self, value):
    #     if not isinstance(value, SzamlaAgentSetting):
    #         raise TypeError("setting must be an SzamlaAgentSetting")
    #     self.__setting = value

    # @property
    # def request(self):
    #     return self.__request
    #
    # @request.setter
    # def request(self, value):
    #     if not isinstance(value, SzamlaAgentRequest):
    #         raise TypeError("setting must be an SzamlaAgentRequest")
    #     self.__request = value

    # @property
    # def response(self):
    #     return self.__response
    #
    # @response.setter
    # def response(self, value):
    #     if not isinstance(value, SzamlaAgentResponse):
    #         raise TypeError("setting must be an SzamlaAgentResponse")
    #     self.__response = value
    #
    # # use as static variable
    agents = {}
    #
    # customHttpHeaders = {}
    # apiUrl = API_URL
    # pdfFileSave = True

    def __init__(self,
                 username,
                 password,
                 api_key,
                 download_pdf=True,
                 log_level=logging.DEBUG,
                 response_type=SzamlaAgentResponse.RESULT_AS_TEXT,
                 aggregator=""
                 ):
        self.setting = SzamlaAgentSetting(username, password, api_key, download_pdf,
                                          SzamlaAgentSetting.DOWNLOAD_COPIES_COUNT, response_type, aggregator)
        self.request = None
        self.response = None
        self.logLevel = log_level
        self.cookieFileName = self.build_cookie_filename()
        self.environment = {}
        self.write_log(f"Szamla Agent initialization finished (apiKey: '{api_key}')", logging.DEBUG)

    # @staticmethod
    # def create(username, password, download_pdf=True, log_level=logging.DEBUG):
    #     index = SzamlaAgent.get_hash(username)
    #
    #     if index not in SzamlaAgent.agents:
    #         SzamlaAgent.agents[index] = SzamlaAgent(username, password, None, download_pdf, log_level)
    #
    #     return SzamlaAgent.agents[index]

    def build_cookie_filename(self):
        filename = 'cookie'
        username = self.setting.username
        apikey = self.setting.api_key

        if username:
            filename += "_" + hashlib.sha1(username.encode('utf-8')).hexdigest()
        elif apikey:
            filename += "_" + hashlib.sha1(apikey.encode('utf-8')).hexdigest()

        return filename + '.txt'

    def send_request(self, request):
        self.request = request
        response = SzamlaAgentResponse(self, request.send())
        return response.handle_response()

    def generate_document(self, request_type, document):
        request = SzamlaAgentRequest(self, request_type, document)
        return self.send_request(request)

    def generate_invoice(self, invoice):
        return self.generate_document('generateInvoice', invoice)

    # def generate_pre_payment_invoice(self, invoice):
    #     return self.generate_invoice(invoice)
    #
    # def generate_final_invoice(self, invoice):
    #     return self.generate_invoice(invoice)
    #
    # def generate_corrective_invoice(self, invoice):
    #     return self.generate_invoice(invoice)
    #
    # def generate_receipt(self, receipt):
    #     return self.generate_document('generateReceipt', receipt)
    #
    # def pay_invoice(self, invoice):
    #     return self.generate_document('payInvoice', invoice)
    #
    # def send_receipt(self, receipt):
    #     return self.generate_document('sendReceipt', receipt)
    #
    # def get_invoice_data(self, data, invoice_type=Invoice.FROM_INVOICE_NUMBER):
    #     invoice = Invoice()
    #
    #     if invoice_type == Invoice.FROM_INVOICE_NUMBER:
    #         invoice.header.invoiceNumber = data
    #     else:
    #         invoice.header.orderNumber = data
    #
    #     if self.is_download_pdf():
    #         message = "Wrong setting for downloading PDF file: please set 'downloadPdf' to true to download invoice."
    #         self.write_log(message, logging.WARN)
    #
    #     self.set_download_pdf(True)
    #     return self.generate_document('requestInvoicePDF', invoice)
    #
    # def is_download_pdf(self):
    #     return self.setting.get_download_pdf()
    #
    # def set_download_pdf(self, download_pdf):
    #     return self.setting.set_download_pdf(download_pdf)

    def write_log(self, message, log_level=logging.DEBUG):
        if self.logLevel < log_level:
            return False

        if self.logLevel != logging.NOTSET:
            logger = logging.Logger("szamla_agent", log_level)
            logger.log(log_level, message)
        return True

    def get_certification_file(self):
        file_name = self.certificationFileName
        if not file_name:
            file_name = AgentConstant.CERTIFICATION_FILENAME
        return SzamlaAgentUtil.get_abs_path(AgentConstant.CERTIFICATION_PATH, file_name)

    # @staticmethod
    # def get_by_instance_id(instance_id):
    #     index = SzamlaAgent.get_hash(instance_id)
    #     agent = SzamlaAgent.agents[index]
    #
    #     if agent is None:
    #         if '@' not in instance_id and instance_id.length() == SzamlaAgentSetting.API_KEY_LENGTH:
    #             raise SzamlaAgentException(SzamlaAgentException.NO_AGENT_INSTANCE_WITH_APIKEY)
    #         else:
    #             raise SzamlaAgentException(SzamlaAgentException.NO_AGENT_INSTANCE_WITH_USERNAME)
    #     return agent

    @staticmethod
    def get_hash(username):
        return hashlib.sha1(username.encode('utf-8')).hexdigest()

    # def set_environment(self, name, url, authorization: dict):
    #     self.environment = {
    #         'name': name,
    #         'url': url,
    #         'auth': authorization
    #     }
    #
    # def has_environment_auth(self):
    #     return self.environment and isinstance(self.environment, dict) and \
    #            self.environment['auth']
    #
    # def get_environment_auth_type(self):
    #     return self.environment['auth']['type'] if self.has_environment_auth() and \
    #                                                self.environment['auth']['type'] else 0
    #
    # def get_environment_auth_user(self):
    #     return self.environment['auth']['user'] if self.has_environment_auth() and \
    #                                                self.environment['auth']['user'] else None
    #
    # def get_environment_auth_password(self):
    #     return self.environment['auth']['password'] if self.has_environment_auth() and \
    #                                                    self.environment['auth']['password'] else None
