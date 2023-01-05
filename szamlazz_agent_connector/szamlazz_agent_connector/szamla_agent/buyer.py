import inspect
from collections import OrderedDict
from html import escape

from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.buyer_ledger import BuyerLedger
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.constant.xml_schema import XmlSchema
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
        self.name = escape(name)
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
            elif field == 'id' \
                    or field == 'email' \
                    or field == 'name' \
                    or field == 'country' \
                    or field == 'zipCode' \
                    or field == 'city' \
                    or field == 'address' \
                    or field == 'taxNumber' \
                    or field == 'taxNumberEU' \
                    or field == 'postalName' \
                    or field == 'postalCountry' \
                    or field == 'postalZip' \
                    or field == 'postalCity' \
                    or field == 'postalAddress' \
                    or field == 'signatoryName' \
                    or field == 'phone' \
                    or field == 'comment':
                SzamlaAgentUtil.check_str_field(field, value, required, type(self).__name__)
        return value

    def __check_fields(self):
        fields = inspect.getmembers(Buyer, lambda a: not (inspect.isroutine(a)))
        fields = [a for a in fields if not (a[0].startswith('__') and a[0].endswith('__'))]
        for item in fields:
            self.__check_field(item[0], item[1])

    def build_xml_data(self, request: SzamlaAgentRequest):
        request_name = request.xmlName
        if request_name == XmlSchema.XML_SCHEMA_CREATE_INVOICE:
            self.__required_fields = {'name': "", 'zip': "", 'city': "", 'address': ""}

            data = OrderedDict([
                ('nev', self.name),
                ('orszag', self.country),
                ('irsz', self.zip_code),
                ('telepules', self.city),
                ('cim', self.address)
            ])

            if self.email:
                data['email'] = self.email
            if self.send_email:
                data['sendEmail'] = self.send_email
            if self.tax_payer:
                data['adoalany'] = self.tax_payer
            if self.tax_number:
                data['adoszam'] = self.tax_number
            if self.tax_number_EU:
                data['adoszamEU'] = self.tax_number_EU
            if self.postal_name:
                data['postazasiNev'] = self.postal_name
            if self.postal_country:
                data['postazasiOrszag'] = self.postal_country
            if self.postal_zip:
                data['postazasiIrsz'] = self.postal_zip
            if self.postal_city:
                data['postazasiTelepules'] = self.postal_city
            if self.postal_address:
                data['postazasiCim'] = self.postal_address
            if self.ledger_data:
                data['vevokonyv'] = self.ledger_data.get_xml_data
            if self.id:
                data['azonosito'] = self.id
            if self.signatory_name:
                data['alairoNeve'] = self.signatory_name
            if self.phone:
                data['telefonszam'] = self.phone
            if self.comment:
                data['megjegyzes'] = self.comment

        elif request_name == XmlSchema.XML_SCHEMA_CREATE_REVERSE_INVOICE:
            data = OrderedDict()
            if self.email:
                data['email'] = self.email
            if self.tax_number:
                data['adoszam'] = self.tax_number
            if self.tax_number_EU:
                data['adoszamEU'] = self.tax_number_EU

        else:
            raise SzamlaAgentException(f"Not existing XML schema: {request_name}")

        self.__check_fields()
        return data
