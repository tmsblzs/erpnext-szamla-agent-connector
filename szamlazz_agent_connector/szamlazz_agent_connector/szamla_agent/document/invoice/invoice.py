import logging
import os

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
    def header(self, value: InvoiceHeader):
        self.__header = value

    @property
    def seller(self):
        return self.__seller

    @seller.setter
    def seller(self, value: Seller):
        self.__seller = value

    @property
    def buyer(self):
        return self.__buyer

    @buyer.setter
    def buyer(self, value: Buyer):
        self.__buyer = value

    @property
    def waybill(self):
        return self.__waybill

    @waybill.setter
    def waybill(self, value: Waybill):
        self.__waybill = value

    @property
    def items(self):
        return self.__items

    @items.setter
    def items(self, value: list):
        self.__items = value

    def add_item(self, item: InvoiceItem):
        self.items.append(item)

    @property
    def credit_notes(self):
        return self.__credit_notes

    @credit_notes.setter
    def credit_notes(self, value: list):
        self.__credit_notes = value

    def add_credit_note(self, credit_note: InvoiceCreditNote):
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
        self.attachments = []
        if header_type:
            self.header = InvoiceHeader(header_type)

    def build_xml_data(self, request: SzamlaAgentRequest):
        xml_name = request.xmlName
        if xml_name == SzamlaAgentRequest.XML_SCHEMA_CREATE_INVOICE:
            data = self.__build_fields_data(request,
                                            ['beallitasok', 'fejlec', 'elado', 'vevo', 'fuvarlevel', 'tetelek'])
        elif xml_name == SzamlaAgentRequest.XML_SCHEMA_DELETE_PROFORMA:
            data = self.__build_fields_data(request, ['beallitasok', 'fejlec'])
        elif xml_name == SzamlaAgentRequest.XML_SCHEMA_CREATE_REVERSE_INVOICE:
            data = self.__build_fields_data(request, ['beallitasok', 'fejlec', 'elado', 'vevo'])
        elif xml_name == SzamlaAgentRequest.XML_SCHEMA_PAY_INVOICE:
            data = self.__build_fields_data(request, ['beallitasok'])
            data = {**data, **self.__build_credits_xml_data()}
        elif xml_name == SzamlaAgentRequest.XML_SCHEMA_REQUEST_INVOICE_XML \
                or SzamlaAgentRequest.XML_SCHEMA_REQUEST_INVOICE_PDF:
            settings = self.__build_fields_data(request, ['beallitasok'])
            data = settings['beallitasok']
        else:
            raise SzamlaAgentException(SzamlaAgentException.XML_SCHEMA_TYPE_NOT_EXISTS + f": {xml_name}")

        return data

    def __build_fields_data(self, request, fields: list):
        data = {}

        for key in fields:
            if key == 'beallitasok':
                value = request.agent.setting.build_xml_data(request)
            elif key == 'fejlec':
                value = self.header.build_xml_data(request)
            elif key == 'tetelek':
                value = self.__build_xml_items_data()
            elif key == 'elado':
                value = self.seller.build_xml_data(request) if self.seller else []
            elif key == 'vevo':
                value = self.buyer.build_xml_data(request) if self.buyer else []
            # elif key == 'fuvarlevel':
            #     value = self.waybill.build_xml_data(request) if self.waybill else []
            else:
                raise SzamlaAgentException(SzamlaAgentException.XML_KEY_NOT_EXISTS + f": {key}")

            if value:
                data[key] = value

        return data

    def __build_xml_items_data(self):
        data = {}
        for key in self.items:
            data[f"item{key}"] = data[key].build_xml_data()
        return data

    def __build_credits_xml_data(self):
        data = {}
        for key in self.credit_notes:
            data[f"note{key}"] = data[key].build_xml_data()
        return data

    def add_attachments(self, file_path):
        if not file_path:
            logging.warning("File name is missing")
        else:
            if len(self.attachments) >= Invoice.INVOICE_ATTACHMENTS_LIMIT:
                raise SzamlaAgentException(f"File attached is failed: {file_path}."
                                           f" Maximum number of attachment is reached."
                                           f"({Invoice.INVOICE_ATTACHMENTS_LIMIT})")
            if not os.path.exists(file_path):
                raise SzamlaAgentException(SzamlaAgentException.ATTACHMENT_NOT_EXISTS + f": {file_path}")

            self.attachments.append(file_path)
