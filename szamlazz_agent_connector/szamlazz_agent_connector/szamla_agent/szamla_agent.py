import hashlib
import logging


from szamlazz_agent_connector.szamlazz_agent_connector.model.constant.agent_constant import AgentConstant
from szamlazz_agent_connector.szamlazz_agent_connector.model.constant.response_constant import ResponseConstant
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.szamla_agent_response import \
     SzamlaAgentResponse
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.szamla_agent_cookie import SzamlaAgentCookie
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.szamla_agent_request import \
     SzamlaAgentRequest
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.szamla_agent_setting import SzamlaAgentSetting
from szamlazz_agent_connector.szamlazz_agent_connector.model.szamla_agent_util import SzamlaAgentUtil


class SzamlaAgent:
    @property
    def setting(self):
        return self._setting

    @property
    def response_type(self):
        return self.setting.response_type

    @response_type.setter
    def response_type(self, value):
        self.setting.response_type = value

    @property
    def download_pdf(self):
        return self.setting.download_pdf

    @download_pdf.setter
    def download_pdf(self, value):
        self.setting.download_pdf = value

    agents = {}

    def __init__(self,
                 username,
                 password,
                 api_key,
                 download_pdf=True,
                 log_level=logging.DEBUG,
                 response_type=ResponseConstant.RESULT_AS_TEXT,
                 aggregator=""
                 ):
        self._setting = SzamlaAgentSetting(username, password, api_key, download_pdf,
                                          SzamlaAgentSetting.DOWNLOAD_COPIES_COUNT, response_type, aggregator)
        self.request = None
        self.response = None
        self.log_level = logging.NOTSET
        self.cookie = SzamlaAgentCookie(self._setting.username, self._setting.api_key)
        self.environment = None
        self.custom_http_headers = None
        self.api_url = AgentConstant.API_URL
        self.pdf_file_save = True
        self.write_log(f"Szamla Agent initialization finished (apiKey: '{api_key}')", logging.DEBUG)
        self.log_email = ''
        self.certification_file_name = AgentConstant.CERTIFICATION_FILENAME

    def send_request(self, request):
        self.request = request
        self.response = SzamlaAgentResponse(self, request.send())
        return self.response.handle_response()

    def generate_document(self, request_type, document):
        request = SzamlaAgentRequest(self, request_type, document)
        return self.send_request(request)

    def generate_invoice(self, invoice):
        return self.generate_document('generateInvoice', invoice)

    def generate_reverse_invoice(self, reverse_invoice):
        return self.generate_document('generateReverseInvoice', reverse_invoice)

    def get_request_entity_header(self):
        header = None

        request = self.request
        entity = request.entity

        from szamlazz_agent_connector.szamlazz_agent_connector.model.document.invoice.invoice import Invoice
        if entity and isinstance(entity, Invoice):
            header = entity.header

        return header

    def write_log(self, message, log_level=logging.DEBUG):
        if self.log_level < log_level:
            return False

        if self.log_level != logging.NOTSET:
            logger = logging.Logger("szamla_agent", log_level)
            logger.log(log_level, message)
        return True

    def get_certification_file(self):
        file_name = self.certification_file_name
        if not file_name:
            file_name = AgentConstant.CERTIFICATION_FILENAME
        return SzamlaAgentUtil.get_abs_path(AgentConstant.CERTIFICATION_PATH, file_name)

    @staticmethod
    def get_hash(username):
        return hashlib.sha1(username.encode('utf-8')).hexdigest()

    def set_environment(self, name, url, authorization: dict):
        self.environment = {
            'name': name,
            'url': url,
            'auth': authorization
        }

    def has_environment_auth(self):
        return self.environment and isinstance(self.environment, dict) and \
               self.environment['auth']

    def get_environment_auth_type(self):
        return self.environment['auth']['type'] if self.has_environment_auth() and \
                                                   self.environment['auth']['type'] else 0

    def get_environment_auth_user(self):
        return self.environment['auth']['user'] if self.has_environment_auth() and \
                                                   self.environment['auth']['user'] else None

    def get_environment_auth_password(self):
        return self.environment['auth']['password'] if self.has_environment_auth() and \
                                                       self.environment['auth']['password'] else None
