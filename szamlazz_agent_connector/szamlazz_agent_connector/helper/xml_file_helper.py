import hashlib
import os

import frappe


class XmlFileHelper:
    @staticmethod
    def create_and_insert_from_agent_result(request, agent_invoice_name):
        xml_file = frappe.new_doc("File")
        xml_file.file_name = os.path.basename(request.xmlFilePath)
        xml_file.file_size = len(request.xmlData)
        xml_file.content_hash = hashlib.md5(request.xmlData).hexdigest()
        xml_file.attached_to_doctype = "SzamlazzAgentConnectorInvoice"
        xml_file.attached_to_field = "xml_file"
        xml_file.file_url = ""
        xml_file.attached_to_name = agent_invoice_name
        xml_file.insert()
        return xml_file
