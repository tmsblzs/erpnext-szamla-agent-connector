import frappe


@frappe.whitelist()
def download(doc_name):
    agent_invoice = frappe.get_last_doc("SzamlazzAgentConnectorInvoice",
                                        filters={"own_invoice_number": doc_name})
    pdf_file = frappe.get_last_doc("File",
                                   filters={"attached_to_name": agent_invoice.name, "attached_to_field": "pdf_file"})
    frappe.response._filename = pdf_file.file_name
    frappe.response.filecontent = pdf_file.get_content()
    frappe.response.type = "pdf"
