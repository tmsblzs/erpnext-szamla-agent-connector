import collections
import inspect
from collections import OrderedDict

from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.constant.xml_schema import XmlSchema
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.exception.szamla_agent_exception import \
    SzamlaAgentException
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.szamla_agent_request import SzamlaAgentRequest
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.szamla_agent_util import SzamlaAgentUtil


class Seller:

    def __init__(self, bank="", bank_account=""):
        self.bank = bank
        self.bank_account = bank_account
        self.email_reply_to = ""
        self.email_subject = ""
        self.email_content = ""
        self.signatory_name = ""
