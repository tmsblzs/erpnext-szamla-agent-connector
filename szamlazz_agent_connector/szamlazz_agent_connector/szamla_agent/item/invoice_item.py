from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.item.item import Item


class InvoiceItem(Item):

    def __init__(self, name, net_unit_price, quantity=Item.DEFAULT_QUANTITY,
                 quantity_unit=Item.DEFAULT_QUANTITY_UNIT, vat=Item.DEFAULT_VAT):
        self.ledger_data = None
        super().__init__(name, net_unit_price, quantity, quantity_unit, vat)
