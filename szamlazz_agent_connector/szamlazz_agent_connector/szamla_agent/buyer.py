import inspect
from collections import OrderedDict
from html import escape

from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.buyer_ledger import BuyerLedger
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.constant.xml_schema import XmlSchema
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.exception.szamla_agent_exception import \
    SzamlaAgentException
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.szamla_agent_request import SzamlaAgentRequest
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.szamla_agent_util import SzamlaAgentUtil


class Buyer:

    def __init__(self, name="", zip_code="", city="", address=""):
        self.id = 0
        self.name = escape(name)
        self.country = ""
        self.zip_code = zip_code
        self.city = city
        self.address = address
        self.email = ""
        self.send_email = True
        self.tax_payer = ""
        self.tax_number = ""
        self.tax_number_EU = ""
        self.postal_name = ""
        self.postal_country = ""
        self.postal_zip = ""
        self.postal_city = ""
        self.postal_address = ""
        self.ledger_data = None
        self.signatory_name = ""
        self.phone = ""
        self.comment = ""
        self.ledger_data = None
        self.__required_fields = {}

