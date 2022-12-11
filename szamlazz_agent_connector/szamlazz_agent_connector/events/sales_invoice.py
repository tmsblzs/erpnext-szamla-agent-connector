from szamlazz_agent_connector.szamlazz_agent_connector.helper.agent_invoice_helper import AgentInvoiceHelper
from szamlazz_agent_connector.szamlazz_agent_connector.helper.invoice_helper import InvoiceHelper
from szamlazz_agent_connector.szamlazz_agent_connector.helper.pdf_file_helper import PdfFileHelper
from szamlazz_agent_connector.szamlazz_agent_connector.helper.reverse_invoice_helper import ReverseInvoiceHelper
from szamlazz_agent_connector.szamlazz_agent_connector.helper.szamla_agent_api_helper import SzamlaAgentApiHelper
from szamlazz_agent_connector.szamlazz_agent_connector.helper.xml_file_helper import XmlFileHelper


def on_submit(doc, event_name):
    invoice = InvoiceHelper.create_from_sales_invoice(doc)

    agent = SzamlaAgentApiHelper.create()
    agent.generate_invoice(invoice)

    _save_result(doc, agent.response)


def _save_result(doc, result):
    pdf_file = PdfFileHelper.create_and_insert_from_agent_result(result)
    agent_invoice = AgentInvoiceHelper.create_and_insert_from_sales_invoice(doc, pdf_file.name,
                                                                            result.get_pdf_file_name(False))
    pdf_file.attached_to_name = agent_invoice.name
    pdf_file.save()
    XmlFileHelper.create_and_insert_from_agent_result(agent_invoice.name)


def on_cancel(doc, event_name):
    reverse_invoice = ReverseInvoiceHelper.create_from_sales_invoice(doc)

    agent = SzamlaAgentApiHelper.create()
    agent.generate_reverse_invoice(reverse_invoice)
