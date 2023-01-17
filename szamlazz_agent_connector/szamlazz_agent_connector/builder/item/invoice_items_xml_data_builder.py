class InvoiceItemsXmlDataBuilder:
    def build_xml_data(self, request, items):
        data = {}
        count = 0
        for item in items:
            count += 1
            from szamlazz_agent_connector.szamlazz_agent_connector.builder.build_xml_data import build_xml_data
            data[f"item{count}"] = build_xml_data(request, item)
        return data
