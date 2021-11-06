import inspect

from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.document.document import Document
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.document.invoice.invoice import Invoice
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.exception.szamla_agent_exception import \
    SzamlaAgentException
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.header.document_header import DocumentHeader
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.szamla_agent_request import SzamlaAgentRequest
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.szamla_agent_util import SzamlaAgentUtil


class InvoiceHeader(DocumentHeader):
    def __init__(self, invoice_type=Invoice.INVOICE_TYPE_P_INVOICE):
        self.invoice_number = ""
        self.invoice_type = 0
        self.issue_date = ""
        self.payment_method = 0
        self.currency = ""
        self.language = ""
        self.fulfillment = ""
        self.payment_due = ""
        self.prefix = ""
        self.extra_logo = ""
        self.correction_to_pay = ""
        self.correctived_number = ""
        self.comment = ""
        self.exchange_bank = ""
        self.exchange_rate = 0
        self.order_number = ""
        self.proforma_number = ""
        self.paid = False
        self.profit_vat = False
        self.invoice_template = Invoice.INVOICE_TEMPLATE_DEFAULT
        self.preview_pdf = False
        self.__required_fields = {}

        if invoice_type:
            self.__set_default(invoice_type)

    def __set_default(self, invoice_type):
        self.invoice = True
        self.invoice_type = invoice_type
        self.issue_date = SzamlaAgentUtil.get_today_str()
        self.payment_method = Document.PAYMENT_METHOD_TRANSFER
        self.currency = Document.get_default_currency()
        self.language = Document.get_default_language()
        self.fulfillment = SzamlaAgentUtil.get_today_str()
        self.payment_due = SzamlaAgentUtil.add_days_to_date(SzamlaAgentUtil.DEFAULT_ADDED_DAYS)

    def __check_field(self, field, value):
        if hasattr(self, field):
            required = True if field in self.__required_fields else False
            if field == 'issueDate' \
                    or field == 'fulfillment' \
                    or field == 'paymentDate':
                SzamlaAgentUtil.check_date_field(field, value, required, type(self).__name__)
            elif field == 'exchangeRate' \
                    or field == 'correctionToPay':
                SzamlaAgentUtil.check_float_field(field, value, required, type(self).__name__)
            elif field == 'proforma' \
                    or field == 'deliveryNote' \
                    or field == 'prePayment' \
                    or field == 'final' \
                    or field == 'reverse' \
                    or field == 'paid' \
                    or field == 'profitVat' \
                    or field == 'corrective':
                SzamlaAgentUtil.check_bool_field(field, value, required, type(self).__name__)
            elif field == 'paymentMehtod' \
                    or field == 'currency' \
                    or field == 'comment' \
                    or field == 'exchangeBank' \
                    or field == 'orderNumber' \
                    or field == 'correctivedNumber' \
                    or field == 'extraLogo' \
                    or field == 'prefix' \
                    or field == 'invoiceNumber':
                SzamlaAgentUtil.check_str_field(field, value, required, type(self).__name__)
            return value

    def __check_fields(self):
        fields = inspect.getmembers(Buyer, lambda a: not (inspect.isroutine(a)))
        fields = [a for a in fields if not (a[0].startswith('__') and a[0].endswith('__'))]
        for item in fields:
            self.__check_field(item[0], item[1])

    def build_xml_data(self, request: SzamlaAgentRequest):
        if not request:
            raise SzamlaAgentException(SzamlaAgentException.XML_DATA_NOT_AVAILABLE)

        self.__required_fields = {
            'invoice_date': "",
            'fulfillment': "",
            'paymentDue': "",
            'paymentMethod': "",
            'currency': "",
            'language': "",
            'buyer': "",
            'items': ""
        }

        data = {
            'keltDatum': self.issue_date,
            'teljesitesDatum': self.fulfillment,
            'fizetesiHataridoDatum': self.payment_due,
            'fizmod': self.payment_method,
            'penznem': self.currency,
            'szamlaNyelve': self.language,
            'megjegyzes': self.comment,
            'arfolyamBank': self.exchange_bank,
            'arfolyam': self.exchange_rate,
            'rendelesSzam': self.order_number,
            'dijbekeroSzamlaszam': self.proforma_number,
            'elolegszamla': self.pre_payment,
            'vegszamla': self.final,
            'helyesbitoszamla': self.corrective,
            'helyesbitettSzamlaszam': self.correctived_number,
            'dijbekero': self.proforma,
            'szallitolevel': self.delivery_note,
            'logoExtra': self.extra_logo,
            'szamlaszamElotag': self.prefix,
            'fizetendoKorrekcio': self.correction_to_pay,
            'fizetve': self.paid,
            'arresAfa': self.profit_vat,
            'szamlaSablon': self.invoice_template,
            'elonezetpdf': self.preview_pdf
        }
        self.__check_fields()
        return data
