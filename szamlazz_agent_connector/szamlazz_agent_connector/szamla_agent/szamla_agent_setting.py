from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.responses.szamla_agent_response import \
    SzamlaAgentResponse


class SzamlaAgentSetting:
    DOWNLOAD_COPIES_COUNT = 1
    API_KEY_LENGTH = 42

    def __init__(self,
                 username,
                 password,
                 api_key,
                 download_pdf=True,
                 copies_count=DOWNLOAD_COPIES_COUNT,
                 response_type=SzamlaAgentResponse.RESULT_AS_TEXT,
                 aggregator=''):
        self.__username = username
        self.__password = password
        self.__api_key = api_key
        self.__download_pdf = download_pdf
        self.__copies_count = copies_count
        self.__response_type = response_type
        self.__aggregator = aggregator

    def set_username(self, username):
        self.__username = username

    def get_username(self):
        return self.__username

    def set_password(self, password):
        self.__password = password

    def get_password(self):
        return self.__password

    def set_api_key(self, api_key):
        self.__api_key = api_key

    def get_api_key(self):
        return self.__api_key

    def set_download_pdf(self, download_pdf):
        self.__download_pdf = download_pdf
        
    def get_download_pdf(self):
        return self.__download_pdf

    def set_copies_count(self, copies_count):
        self.__copies_count = copies_count

    def get_copies_count(self):
        return self.__copies_count

    def set_response_type(self, response_type):
        self.__response_type = response_type

    def get_response_type(self):
        return self.__response_type

    def set_aggregator(self, aggregator):
        self.__aggregator = aggregator

    def get_aggregator(self):
        return self.__aggregator
