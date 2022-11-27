import hashlib
import os

import dateutil.utils

import frappe
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.buyer import Buyer
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.constant.document_constant import DocumentConstant
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.constant.invoice_constant import InvoiceConstant
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.constant.tax_payer_constant import TaxPayerConstant
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.document.invoice.invoice import Invoice
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.document.invoice.reverse_invoice import \
    ReverseInvoice
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.header.reverse_invoice_header import \
    ReverseInvoiceHeader
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.item.invoice_item import InvoiceItem
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.seller import Seller
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.szamla_agent_api import SzamlaAgentApi
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.szamla_agent_util import SzamlaAgentUtil


def on_submit(doc, event_name):

    connection_settings = frappe.get_doc('SzamlazzAgentConnectorSetting')

    agent = SzamlaAgentApi.create(connection_settings.apikey)
    # agent.setting.response_type = ResponseConstant.RESULT_AS_XML

    invoice = Invoice(InvoiceConstant.INVOICE_TYPE_P_INVOICE)

    header = invoice.header
    header.payment_method = DocumentConstant.PAYMENT_METHOD_TRANSFER
    header.fulfillment = doc.fullfilment_date
    header.payment_due = doc.due_date
    header.prefix = ''
    header.preview_pdf = False
    header.invoice_template = InvoiceConstant.INVOICE_TEMPLATE_DEFAULT

    seller = _get_seller(doc)
    invoice.seller = seller

    buyer = _get_buyer(doc)
    invoice.buyer = buyer

    for item in doc.items:
        stock_item = frappe.get_doc("Item", item.item_code)
        tax = [x for x in stock_item.taxes if x.tax_category == 'ÁFA']
        tax_rate = 0
        if tax:
            tax_template = frappe.get_doc("Item Tax Template", tax[0].item_tax_template)
            if tax_template:
                tax_rate = tax_template.taxes[0].tax_rate
        invoice_item = InvoiceItem(item.item_name, item.net_rate, item.stock_qty, item.stock_uom, str(tax_rate))
        invoice_item.net_price = item.net_amount
        invoice_item.vat_amount = item.net_amount * (tax_rate / 100)
        invoice_item.gross_amount = invoice_item.net_price + invoice_item.vat_amount
        invoice.add_item(invoice_item)

    agent.generate_invoice(invoice)
    result = agent.response

    pdf_file = frappe.new_doc("File")
    pdf_file.file_name = result.get_pdf_file_name(False)
    pdf_file.file_size = len(result.pdfFile)
    pdf_file.content_hash = hashlib.md5(result.pdfFile).hexdigest()
    pdf_file.attached_to_doctype = "SzamlazzAgentConnectorInvoice"
    pdf_file.attached_to_field = "pdf_file"
    pdf_file.file_url = ""
    pdf_file.insert()

    request = agent.request
    xml_file = frappe.new_doc("File")
    xml_file.file_name = os.path.basename(request.xmlFilePath)
    xml_file.file_size = len(request.xmlData)
    xml_file.content_hash = hashlib.md5(request.xmlData).hexdigest()
    xml_file.attached_to_doctype = "SzamlazzAgentConnectorInvoice"
    xml_file.attached_to_field = "xml_file"
    xml_file.file_url = ""
    xml_file.insert()

    agent_invoice = frappe.new_doc("SzamlazzAgentConnectorInvoice")
    agent_invoice.buyer = doc.customer
    agent_invoice.created_at = dateutil.utils.today()
    agent_invoice.pdf_file = pdf_file.name
    agent_invoice.invoice_date = doc.posting_date
    agent_invoice.sum = doc.base_net_total
    agent_invoice.is_successfully_send = True
    agent_invoice.own_invoice_number = doc.name
    agent_invoice.szamlazz_invoice_number = os.path.splitext(pdf_file.file_name)[0]
    agent_invoice.sales_invoice = doc.name
    agent_invoice.insert()

    pdf_file.attached_to_name = agent_invoice.name
    pdf_file.save()
    xml_file.attached_to_name = agent_invoice.name
    xml_file.save()


def _get_buyer(doc):
    customer_name = doc.customer
    customer = frappe.get_doc('Customer', customer_name)
    customer_address = frappe.get_doc('Address', doc.customer_address)
    buyer = Buyer(customer_name, customer_address.pincode, customer_address.city, customer_address.address_line1)
    buyer.tax_number = customer.tax_id
    buyer.tax_payer = TaxPayerConstant.TAXPAYER_HAS_TAXNUMBER
    return buyer


def _get_seller(doc):
    company_name = doc.company
    company = frappe.get_doc('Company', company_name)
    bank_accounts = frappe.get_all('Bank Account', filters={'account': company.default_bank_account})
    bank_account = frappe.get_doc('Bank Account', bank_accounts[0])
    seller = Seller(bank_account.bank, bank_account.bank_account_no)
    return seller


def on_cancel(doc, event_name):
    connection_settings = frappe.get_doc('SzamlazzAgentConnectorSetting')
    agent_invoice = frappe.get_all('SzamlazzAgentConnectorInvoice',  filters={'own_invoice_number': doc.name})
    if not agent_invoice:
        raise TypeError("Szamlazz Agent Invoice not found!")
    invoice = frappe.get_doc("SzamlazzAgentConnectorInvoice", agent_invoice[0])
    if not invoice:
        raise TypeError("Invoice not found!")
    reverse_invoice = ReverseInvoice()
    header = reverse_invoice.header
    header.invoice_number = invoice.szamlazz_invoice_number.upper()
    # header.issue_date = SzamlaAgentUtil.get_date_str(invoice.invoice_date)
    # header.fulfillment = SzamlaAgentUtil.get_date_str(doc.fullfilment_date)
    header.invoice_template = InvoiceConstant.INVOICE_TEMPLATE_DEFAULT

    agent = SzamlaAgentApi.create(connection_settings.apikey)
    agent.generate_reverse_invoice(reverse_invoice)