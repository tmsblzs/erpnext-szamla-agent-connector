from collections import OrderedDict

from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.item.invoice_item import InvoiceItem
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.szamla_agent_util import SzamlaAgentUtil


class InvoiceItemXmlDataBuilder:
    def build_xml_data(self, item: InvoiceItem):
        self.check_fields()

        data = OrderedDict([
            ('megnevezes', item.name),
            ('mennyiseg', SzamlaAgentUtil.float_format(item.quantity)),
            ('mennyisegiEgyseg', item.quantity_unit),
            ('nettoEgysegar', SzamlaAgentUtil.float_format(item.net_unit_price)),
            ('afakulcs', item.vat),
            ('nettoErtek', SzamlaAgentUtil.float_format(item.net_price)),
            ('afaErtek', SzamlaAgentUtil.float_format(item.vat_amount)),
            ('bruttoErtek', SzamlaAgentUtil.float_format(item.gross_amount))
        ])

        if item.id:
            data['azonosito'] = item.id
        if item.comment:
            data['megjegyzes'] = item.comment
        if item.ledger_data:
            data['tetelFokonyv'] = item.ledger_data.build_xml_data()
        return data
