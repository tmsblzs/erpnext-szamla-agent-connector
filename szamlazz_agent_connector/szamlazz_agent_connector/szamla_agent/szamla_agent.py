import logging

from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.responses.szamla_agent_response import \
    SzamlaAgentResponse
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.szamla_agent_request import \
    SzamlaAgentRequest
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.szamla_agent_setting import SzamlaAgentSetting


class SzamlaAgent:
    API_VERSION = '2.10.2'
    API_URL = 'https://www.szamlazz.hu/szamla/'
    CHARSET = 'UTF-8'
    COOKIE_FILENAME = 'cookie.txt'
    CERTIFICATION_FILENAME = 'cacert.pem'
    CERTIFICATION_PATH = './cert'
    PDF_FILE_SAVE_PATH = './pdf'
    XML_FILE_SAVE_PATH = './xmls'
    ATTACHMENTS_SAVE_PATH = './attachments'

    logLevel = 'OFF'
    logEmail = ''

    callMethod = SzamlaAgentRequest.CALL_METHOD_AUTO
    certificationFileName = CERTIFICATION_FILENAME
    cookieFileName = COOKIE_FILENAME

    setting = None
    request = None
    response = None

    # use as static variable
    agents = []

    customHttpHeaders = []
    apiUrl = API_URL
    pdfFileSave = True
    environment = []

    def __init__(self,
                 username,
                 password,
                 api_key,
                 download_pdf=True,
                 log_level='DEBUG',
                 response_type=SzamlaAgentResponse.RESULT_AS_TEXT,
                 aggregator=""
                 ):
        self.setting = SzamlaAgentSetting(username, password, api_key, download_pdf,
                                          SzamlaAgentSetting.DOWNLOAD_COPIES_COUNT, response_type, aggregator)
        self.logLevel = log_level
        self.cookieFileName = self.build_cookie_filename()
        self.write_log("Szamla Agent initialization finished (" + 'apiKey: ' + api_key + ")", 'DEBUG')

    def get_hash(self):
        return hash(self.username)

    def build_cookie_filename(self):
        filename = 'cookie'
        username = self.setting.get_username()
        apikey = self.setting.get_api_key()

        if len(username) != 0:
            filename += "_" + hash(username)
        elif len(apikey) != 0:
            filename += "_" + hash(apikey)

        return filename + '.txt'

    def send_request(self, request):
        self.request = request
        response = SzamlaAgentResponse()

    def write_log(self, message, log_level=logging.DEBUG):
        if self.logLevel < log_level:
            return False

        if self.logLevel != logging.NOTSET:
            logger = logging.Logger("szamla_agent", log_level)
            logger.log(log_level, message)
        return True
