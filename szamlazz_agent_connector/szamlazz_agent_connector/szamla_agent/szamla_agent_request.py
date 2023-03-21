from szamlazz_agent_connector.szamlazz_agent_connector.model.constant.xml_schema import XmlSchema
from szamlazz_agent_connector.szamlazz_agent_connector.model.document.document import Document
from szamlazz_agent_connector.szamlazz_agent_connector.model.document.invoice.invoice import Invoice
from szamlazz_agent_connector.szamlazz_agent_connector.model.document.invoice.reverse_invoice import ReverseInvoice


class SzamlaAgentRequest:
    def __init__(self, agent, request_type, entity: Document):
        self.agent = agent
        self.request_type = request_type
        self.entity = entity
        self.c_data = True



