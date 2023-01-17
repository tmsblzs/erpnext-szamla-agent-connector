from szamlazz_agent_connector.szamlazz_agent_connector.model.document.document import Document


class SzamlaAgentRequest:
    def __init__(self, agent, request_type, entity: Document):
        self.agent = agent
        self.request_type = request_type
        self.entity = entity
        self.c_data = True


