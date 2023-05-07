from szamlazz_agent_connector.szamlazz_agent_connector.model.document.document import Document


class SzamlaAgentRequest:
    def __init__(self, agent, request_type, entity: Document):
        self.agent = agent
        self.request_type = request_type
        self.entity = entity
        self.c_data = True

    def get_entity_header(self):
        header = None

        entity = self.entity

        from szamlazz_agent_connector.szamlazz_agent_connector.model.document.invoice.invoice import Invoice
        if entity and isinstance(entity, Invoice):
            header = entity.header

        return header

