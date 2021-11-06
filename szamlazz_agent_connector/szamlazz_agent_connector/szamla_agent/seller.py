import inspect

from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.exception.szamla_agent_exception import \
    SzamlaAgentException
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.szamla_agent_request import SzamlaAgentRequest
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.szamla_agent_util import SzamlaAgentUtil


class Seller:
    def __int__(self, bank="", bank_account=""):
        self.bank = bank
        self.bank_account = bank_account
        self.email_reply_to = ""
        self.email_subject = ""
        self.email_content = ""
        self.signatory_name = ""

    def __check_field(self, field, value):
        if hasattr(self, field):
            if field == 'bank' \
                    or field == 'bankAccount' \
                    or field == 'emailReplyTo' \
                    or field == 'emailSubject' \
                    or field == 'emailContent' \
                    or field == 'signatoryName':
                SzamlaAgentUtil.check_str_field(field, value, false, type(self).__name__)
        return value

    def __check_fields(self):
        fields = inspect.getmembers(Seller, lambda a: not (inspect.isroutine(a)))
        fields = [a for a in fields if not (a[0].startswith('__') and a[0].endswith('__'))]
        for item in fields:
            self.__check_field(item[0], item[1])

    def build_xml_data(self, request: SzamlaAgentRequest):
        self.__check_fields()
        request_name = request.xmlName

        if request_name == SzamlaAgentRequest.XML_SCHEMA_CREATE_INVOICE:
            data = {
                'bank': self.bank,
                'bankszamlaszam': self.bank_account,
                'alaironeve': self.signatory_name
            }

            email_data = self.__get_xml_email_data()
            if email_data:
                data = {**data, **email_data}
        elif request_name == SzamlaAgentRequest.XML_SCHEMA_CREATE_REVERSE_INVOICE:
            data = self.__get_xml_email_data()
        else:
            raise SzamlaAgentException(SzamlaAgentException.XML_SCHEMA_TYPE_NOT_EXISTS + f": {request_name}")
        return data

    def __get_xml_email_data(self):
        data = {
            'emailReplyto': self.email_reply_to,
            'emailTargy': self.email_subject,
            'emailSzoveg': self.email_content
        }
        return data
