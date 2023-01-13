import inspect
from collections import OrderedDict

from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.header.invoice_header import InvoiceHeader
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.szamla_agent_util import SzamlaAgentUtil


class InvoiceHeaderXmlBuilder:
    def __init__(self):
        self._required_fields = {
            'invoice_date': "",
            'fulfillment': "",
            'paymentDue': "",
            'paymentMethod': "",
            'currency': "",
            'language': "",
            'buyer': "",
            'items': ""
        }

    def _check_field(self, field, value):
        if hasattr(self, field):
            required = True if field in self._required_fields else False
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

    def _check_fields(self):
        self.check_fields()

    def check_fields(self):
        fields = inspect.getmembers(InvoiceHeader, lambda a: not (inspect.isroutine(a)))
        fields = [a for a in fields if not (a[0].startswith('__') and a[0].endswith('__'))]
        for item in fields:
            self._check_field(item[0], item[1])

    def build_xml_data(self, header: InvoiceHeader):
        data = OrderedDict([
            ('keltDatum', header.issue_date),
            ('teljesitesDatum', header.fulfillment),
            ('fizetesiHataridoDatum', header.payment_due),
            ('fizmod', header.payment_method),
            ('penznem', header.currency),
            ('szamlaNyelve', header.language)
        ])

        if header.comment:
            data['megjegyzes'] = header.comment
        if header.exchange_bank:
            data['arfolyamBank'] = header.exchange_bank
        if header.exchange_rate:
            data['arfolyam'] = SzamlaAgentUtil.float_format(header.exchange_rate)
        if header.order_number:
            data['rendelesSzam'] = header.order_number
        if header.proforma_number:
            data['dijbekeroSzamlaszam'] = header.proforma_number
        if header.pre_payment:
            data['elolegszamla'] = header.pre_payment
        if header.final:
            data['vegszamla'] = header.final
        if header.corrective:
            data['helyesbitoszamla'] = header.corrective
        if header.correctived_number:
            data['helyesbitettSzamlaszam'] = header.correctived_number
        if header.proforma:
            data['dijbekero'] = header.proforma
        if header.delivery_note:
            data['szallitolevel'] = header.delivery_note
        if header.exchange_bank:
            data['logoExtra'] = header.extra_logo
        if header.prefix:
            data['szamlaszamElotag'] = header.prefix
        if header.correction_to_pay:
            data['fizetendoKorrekcio'] = header.correction_to_pay
        if header.paid:
            data['fizetve'] = header.paid
        if header.profit_vat:
            data['arresAfa'] = header.profit_vat
        if header.invoice_template:
            data['szamlaSablon'] = header.invoice_template
        if header.preview_pdf:
            data['elonezetpdf'] = header.preview_pdf

        self._check_fields()
        return data
