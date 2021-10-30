from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.buyer import Buyer
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.credit_note.invoice_credit_note import \
    InvoiceCreditNote
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.document.document import Document
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.exception.szamla_agent_exception import \
    SzamlaAgentException
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.header.invoice_header import InvoiceHeader
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.item.invoice_item import InvoiceItem
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.seller import Seller
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.szamla_agent_request import SzamlaAgentRequest
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.waybill.waybill import Waybill


class Invoice(Document):

    # Számla típus: papír számla 
    INVOICE_TYPE_P_INVOICE = 1

    # Számla típus: e-számla 
    INVOICE_TYPE_E_INVOICE = 2

    # Számla lekérdezése számlaszám alapján 
    FROM_INVOICE_NUMBER = 1

    # Számla lekérdezése rendelési szám alapján 
    FROM_ORDER_NUMBER = 2

    # Jóváírások maximális száma
    # a számla kifizetettségének beállításakor
    CREDIT_NOTES_LIMIT = 5

    # Számlához csatolandó fájlok maximális száma 
    INVOICE_ATTACHMENTS_LIMIT = 5

    # Számlázz.hu ajánlott számlakép 
    INVOICE_TEMPLATE_DEFAULT = 'SzlaMost'

    # Tradicionális számlakép 
    INVOICE_TEMPLATE_TRADITIONAL = 'SzlaAlap'

    # Borítékbarát számlakép 
    INVOICE_TEMPLATE_ENV_FRIENDLY = 'SzlaNoEnv'

    # Hőnyomtatós számlakép (8 cm széles) 
    INVOICE_TEMPLATE_8CM = 'Szla8cm'

    # Retró kéziszámla számlakép 
    INVOICE_TEMPLATE_RETRO = 'SzlaTomb'

    @property
    def header(self):
        return self.__header

    @header.setter
    def header(self, value):
        if not isinstance(value, InvoiceHeader):
            raise TypeError("header must be an InvoiceHeader")
        self.__header = value

    @property
    def seller(self):
        return self.__seller

    @seller.setter
    def seller(self, value):
        if not isinstance(value, Seller):
            raise TypeError("seller must be an Seller")
        self.__seller = value

    @property
    def buyer(self):
        return self.__buyer

    @buyer.setter
    def buyer(self, value):
        if not isinstance(value, Buyer):
            raise TypeError("buyer must be an Buyer")
        self.__buyer = value

    @property
    def waybill(self):
        return self.__waybill

    @waybill.setter
    def waybill(self, value):
        if not isinstance(value, Waybill):
            raise TypeError("waybill must be an Waybill")
        self.__buyer = value

    @property
    def items(self):
        return self.__items

    @items.setter
    def items(self, value):
        if not isinstance(value, list):
            raise TypeError("items must be an array")
        return self.__items

    def add_item(self, item):
        if not isinstance(item, InvoiceItem):
            raise TypeError("item must be an InvoiceItem")
        self.items.append(item)

    @property
    def credit_notes(self):
        return self.__credit_notes

    @credit_notes.setter
    def credit_notes(self, value):
        if not isinstance(value, list):
            raise TypeError("credit_notes must be an array")
        self.__credit_notes = value

    def add_credit_note(self, credit_note):
        if not isinstance(credit_note, InvoiceCreditNote):
            raise TypeError("credit_note must be an InvoiceCreditNote")

        if len(self.credit_notes) < Invoice.CREDIT_NOTES_LIMIT:
            self.__credit_notes.append(credit_note)

    @property
    def is_additive(self):
        return self.__is_additive

    @is_additive.setter
    def is_additive(self, value):
        self.__is_additive = value

    def __init__(self, header_type=INVOICE_TYPE_P_INVOICE):
        self.seller = None
        self.buyer = None
        self.waybill = None
        self.items = None
        self.credit_notes = None
        self.is_additive = True
        if header_type:
            self.header = InvoiceHeader(header_type)

    def build_xml_data(self, request):
        if not isinstance(request, SzamlaAgentRequest):
            raise TypeError("request must be an SzamlaAgentRequest")

        xml_name = request.xmlName
        if xml_name == SzamlaAgentRequest.XML_SCHEMA_CREATE_INVOICE:
            data = self.__build_fields_data(request, ['beallitasok', 'fejlec', 'elado', 'vevo', 'fuvarlevel', 'tetelek'])
        elif xml_name == SzamlaAgentRequest.XML_SCHEMA_DELETE_PROFORMA:
            data = self.__build_fields_data(request, ['beallitasok', 'fejlec'])
        elif xml_name == SzamlaAgentRequest.XML_SCHEMA_CREATE_REVERSE_INVOICE:
            data = self.__build_fields_data(request, ['beallitasok', 'fejlec', 'elado', 'vevo'])
        elif xml_name == SzamlaAgentRequest.XML_SCHEMA_PAY_INVOICE:
            data = self.__build_fields_data(request, ['beallitasok'])
            data = data + self.__build_credits_xml_data()
        elif xml_name == SzamlaAgentRequest.XML_SCHEMA_REQUEST_INVOICE_XML \
                or SzamlaAgentRequest.XML_SCHEMA_REQUEST_INVOICE_PDF:
            settings = self.__build_fields_data(request, ['beallitasok'])
            data = settings['beallitasok']
        else:
            raise SzamlaAgentException(SzamlaAgentException.XML_SCHEMA_TYPE_NOT_EXISTS + f": {xml_name}")

        return data

    def __build_fields_data(self, request, fields):
        return []

    def __build_credits_xml_data(self):
        return []

