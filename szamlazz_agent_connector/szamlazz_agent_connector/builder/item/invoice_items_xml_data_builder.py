from szamlazz_agent_connector.szamlazz_agent_connector.builder.item.invoice_item_xml_data_builder import \
    InvoiceItemXmlDataBuilder


class InvoiceItemsXmlDataBuilder:
    def __init__(self):
        self._item_builder = InvoiceItemXmlDataBuilder()

    def build_xml_data(self, request, items):
        data = {}
        count = 0
        for item in items:
            count += 1
            data[f"item{count}"] = self._item_builder.build_xml_data(item)
        return data
