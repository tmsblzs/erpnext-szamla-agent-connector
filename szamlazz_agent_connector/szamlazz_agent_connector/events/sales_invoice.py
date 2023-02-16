from szamlazz_agent_connector.szamlazz_agent_connector.helper.agent.agent_invoice_helper import AgentInvoiceHelper
from szamlazz_agent_connector.szamlazz_agent_connector.helper.document.invoice_helper import InvoiceHelper
from szamlazz_agent_connector.szamlazz_agent_connector.helper.file.pdf_file_helper import PdfFileHelper
from szamlazz_agent_connector.szamlazz_agent_connector.helper.document.reverse_invoice_helper \
    import ReverseInvoiceHelper
from szamlazz_agent_connector.szamlazz_agent_connector.helper.file.xml_file_helper import XmlFileHelper
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.document_generate import document_generate


def on_submit(doc, event_name):
    invoice = InvoiceHelper.create_from_sales_invoice(doc)

    response = document_generate(invoice)

    # _save_result(doc, agent.request, agent.response)


def on_cancel(doc, event_name):
    reverse_invoice = ReverseInvoiceHelper.create_from_sales_invoice(doc)

    response = document_generate(reverse_invoice)


def _save_result(doc, request, result):
    pdf_file = PdfFileHelper.create_and_insert_from_agent_result(result)
    agent_invoice = AgentInvoiceHelper.create_and_insert_from_sales_invoice(doc, pdf_file.name,
                                                                            result.get_pdf_file_name(False))
    pdf_file.attached_to_name = agent_invoice.name
    pdf_file.save()
    XmlFileHelper.create_and_insert_from_agent_result(request, agent_invoice.name)


