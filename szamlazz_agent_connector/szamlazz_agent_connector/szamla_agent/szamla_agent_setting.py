from szamlazz_agent_connector.szamlazz_agent_connector.model.constant.response_constant import ResponseConstant


class SzamlaAgentSetting:
    DOWNLOAD_COPIES_COUNT = 1
    API_KEY_LENGTH = 42

    def __init__(self,
                 username,
                 password,
                 api_key,
                 download_pdf=True,
                 copies_count=DOWNLOAD_COPIES_COUNT,
                 response_type=ResponseConstant.RESULT_AS_TEXT,
                 aggregator=''):
        self.username = username
        self.password = password
        self.api_key = api_key
        self.download_pdf = download_pdf
        self.copies_count = copies_count
        self.response_type = response_type
        self.aggregator = aggregator
        self.guardian = False
        self.keychain = ""

