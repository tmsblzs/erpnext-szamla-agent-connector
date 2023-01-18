import inspect
from collections import OrderedDict

from szamlazz_agent_connector.szamlazz_agent_connector.model.header.invoice_header import InvoiceHeader
from szamlazz_agent_connector.szamlazz_agent_connector.model.szamla_agent_util import SzamlaAgentUtil
from szamlazz_agent_connector.szamlazz_agent_connector.validator.header.invoice_header_validator import \
    InvoiceHeaderValidator


class InvoiceHeaderXmlDataBuilder:
    def __init__(self):
        self._validator = InvoiceHeaderValidator()

    def build_xml_data(self, request, header: InvoiceHeader):
        self._validator.check_fields(header)

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

        return data
