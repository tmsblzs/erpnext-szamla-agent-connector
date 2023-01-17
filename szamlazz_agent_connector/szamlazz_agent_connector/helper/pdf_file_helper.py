import hashlib

import frappe


class PdfFileHelper:
    @staticmethod
    def create_and_insert_from_agent_result(result):
        pdf_file = frappe.new_doc("File")
        pdf_file.file_name = result.get_pdf_file_name(False)
        pdf_file.file_size = len(result.pdf_file)
        pdf_file.content_hash = hashlib.md5(result.pdf_file).hexdigest()
        pdf_file.attached_to_doctype = "SzamlazzAgentConnectorInvoice"
        pdf_file.attached_to_field = "pdf_file"
        pdf_file.file_url = ""
        pdf_file.insert()
        return pdf_file
