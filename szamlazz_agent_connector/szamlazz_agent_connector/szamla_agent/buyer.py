import inspect

from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.buyer_ledger import BuyerLedger
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.exception.szamla_agent_exception import \
    SzamlaAgentException
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.szamla_agent_request import SzamlaAgentRequest
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.szamla_agent_util import SzamlaAgentUtil


class Buyer:
    @property
    def ledger_data(self):
        return self.__ledger_data

    @ledger_data.setter
    def ledger_data(self, value: BuyerLedger):
        self.__ledger_data = value

    def __init__(self, name="", zip_code="", city="", address=""):
        self.id = 0
        self.name = name
        self.country = ""
        self.zip_code = zip_code
        self.city = city
        self.address = address
        self.email = ""
        self.send_email = True
        self.tax_payer = ""
        self.tax_number = ""
        self.tax_number_EU = ""
        self.postal_name = ""
        self.postal_country = ""
        self.postal_zip = ""
        self.postal_city = ""
        self.postal_address = ""
        self.ledger_data = None
        self.signatory_name = ""
        self.phone = ""
        self.comment = ""
        self.__required_fields = {}

    def __check_field(self, field, value):
        if hasattr(self, field):
            required = True if field in self.__required_fields else False
            if field == 'taxPayer':
                SzamlaAgentUtil.check_int_field(field, value, required, type(self).__name__)
            elif field == 'sendEmail':
                SzamlaAgentUtil.check_bool_field(field, value, required, type(self).__name__)
            else:
                SzamlaAgentUtil.check_str_field(field, value, required, type(self).__name__)
        return value

    def __check_fields(self):
        fields = inspect.getmembers(Buyer, lambda a: not (inspect.isroutine(a)))
        fields = [a for a in fields if not (a[0].startswith('__') and a[0].endswith('__'))]
        for item in fields:
            self.__check_field(item[0], item[1])

    def build_xml_data(self, request: SzamlaAgentRequest):
        request_name = request.xmlName
        if request_name == SzamlaAgentRequest.XML_SCHEMA_CREATE_INVOICE:
            self.__required_fields = {'name': "", 'zip': "", 'city': "", 'address': ""}

            data = {
                'nev': self.name,
                'orszag': self.country,
                'irsz': self.zip_code,
                'telepules': self.city,
                'cim': self.address,
                'email': self.email,
                'sendEmail': self.send_email,
                'adoalany': self.tax_payer,
                'adoszam': self.tax_number,
                'adoszamEU': self.tax_number_EU,
                'postazasiNev': self.postal_name,
                'postazasiOrszag': self.postal_country,
                'postazasiIrsz': self.postal_zip,
                'postazasiTelepules': self.postal_city,
                'postazasiCim': self.postal_address,
                'vevokonyv': self.ledger_data.get_xml_data if self.ledger_data else "",
                'azonosito': self.id,
                'alairoNeve': self.signatory_name,
                'telefonszam': self.phone,
                'megjegyzes': self.comment,
            }
        elif request_name == SzamlaAgentRequest.XML_SCHEMA_CREATE_REVERSE_INVOICE:
            data = {
                'email': self.email,
                'adoszam': self.tax_number,
                'adoszamEU': self.tax_number_EU
            }
        else:
            raise SzamlaAgentException(f"Not existing XML schema: {request_name}")

        self.__check_fields()
        return data
