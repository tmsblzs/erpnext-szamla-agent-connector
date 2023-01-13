import logging
import os

from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.constant.invoice_constant import InvoiceConstant
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.constant.xml_schema import XmlSchema
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.document.document import Document
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.exception.szamla_agent_exception import \
    SzamlaAgentException
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.header.invoice_header import InvoiceHeader
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.item.invoice_item import InvoiceItem


class Invoice(Document):

    @property
    def items(self):
        return self._items

    def add_item(self, item: InvoiceItem):
        self.items.append(item)

    def __init__(self, seller, buyer, header_type=InvoiceConstant.INVOICE_TYPE_P_INVOICE):
        self.seller = seller
        self.buyer = buyer
        self.waybill = None
        self._items = []
        self._credit_notes = None
        self._is_additive = True
        self.attachments = []
        if header_type:
            self.header = InvoiceHeader(header_type)

    def add_attachments(self, file_path):
        if not file_path:
            logging.warning("File name is missing")
        else:
            if len(self.attachments) >= InvoiceConstant.INVOICE_ATTACHMENTS_LIMIT:
                raise SzamlaAgentException(f"File attached is failed: {file_path}."
                                           f" Maximum number of attachment is reached."
                                           f"({InvoiceConstant.INVOICE_ATTACHMENTS_LIMIT})")
            if not os.path.exists(file_path):
                raise SzamlaAgentException(SzamlaAgentException.ATTACHMENT_NOT_EXISTS + f": {file_path}")

            self.attachments.append(file_path)
