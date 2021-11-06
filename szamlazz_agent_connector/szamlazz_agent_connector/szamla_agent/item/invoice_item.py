from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.item.item import Item
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.ledger.invoice_item_ledger import InvoiceItemLedger
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.szamla_agent_util import SzamlaAgentUtil


class InvoiceItem(Item):

    @property
    def ledger_data(self):
        return self.__ledger_data

    @ledger_data.setter
    def ledger_data(self, value: InvoiceItemLedger):
        self.__ledger_data = value

    def __init__(self, name, net_unit_price, quantity=Item.DEFAULT_QUANTITY,
                 quantity_unit=Item.DEFAULT_QUANTITY_UNIT, vat=Item.DEFAULT_VAT):
        self.ledger_data = None
        super().__init__(name, net_unit_price, quantity, quantity_unit, vat)

    def build_xml_data(self):
        data = {}
        self.__check_fields()

        data = {
            'megnevezes': self.name,
            'mennyiseg': SzamlaAgentUtil.float_format(self.quantity),
            'mennyisegiEgyseg': self.quantity_unit,
            'nettoEgysegar': SzamlaAgentUtil.float_format(self.net_unit_price),
            'afakulcs': self.vat,
            'nettoErtek': SzamlaAgentUtil.float_format(self.net_price),
            'afaErtek': SzamlaAgentUtil.float_format(self.vat_amount),
            'bruttoErtek': SzamlaAgentUtil.float_format(self.gross_amount)
        }

        if self.id:
            data['azonosito'] = self.id
        if self.comment:
            data['megjegyzes'] = self.comment
        if self.ledger_data:
            data['tetelFokonyv'] = self.ledger_data.build_xml_data()
        return data
