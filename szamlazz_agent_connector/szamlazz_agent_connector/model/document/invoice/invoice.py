import logging
import os

from szamlazz_agent_connector.szamlazz_agent_connector.model.constant.document_constant import DocumentConstant
from szamlazz_agent_connector.szamlazz_agent_connector.model.constant.invoice_constant import InvoiceConstant
from szamlazz_agent_connector.szamlazz_agent_connector.model.constant.xml_schema import XmlSchema
from szamlazz_agent_connector.szamlazz_agent_connector.model.document.document import Document
from szamlazz_agent_connector.szamlazz_agent_connector.model.exception.szamla_agent_exception import \
    SzamlaAgentException
from szamlazz_agent_connector.szamlazz_agent_connector.model.header.invoice_header import InvoiceHeader
from szamlazz_agent_connector.szamlazz_agent_connector.model.item.invoice_item import InvoiceItem


class Invoice(Document):

    @property
    def items(self):
        return self._items

    def add_item(self, item: InvoiceItem):
        self.items.append(item)

    @property
    def xml_name(self):
        return self._xml_name

    @property
    def xsd_dir(self):
        return self._xsd_dir

    @property
    def is_attachments(self):
        return len(self.attachments) > 0

    def __init__(self, seller, buyer, header_type=InvoiceConstant.INVOICE_TYPE_P_INVOICE):
        super().__init__()
        self.seller = seller
        self.buyer = buyer
        self.waybill = None
        self._items = []
        self.credit_notes = None
        self.is_additive = True
        self._file_name = 'action-xmlagentxmlfile'
        self._xml_name = XmlSchema.XML_SCHEMA_CREATE_INVOICE
        self._xml_schema_type = DocumentConstant.DOCUMENT_TYPE_INVOICE
        self._xsd_dir = 'agent'

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
