import ast
import json

import frappe
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.buyer import Buyer
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.constant.document_constant import DocumentConstant
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.constant.invoice_constant import InvoiceConstant
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.constant.response_constant import ResponseConstant
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.constant.tax_payer_constant import TaxPayerConstant
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.document.invoice.invoice import Invoice
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.item.invoice_item import InvoiceItem
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.seller import Seller
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.szamla_agent_api import SzamlaAgentApi


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

    company_name = doc.company
    company = frappe.get_doc('Company', company_name)
    bank_account = frappe.get_doc('Bank Account', 'PENSAV-BankAccount - OTP BANK Nyrt')
    seller = Seller(bank_account.bank, bank_account.bank_account_no)
    invoice.seller = seller

    customer_name = doc.customer
    customer = frappe.get_doc('Customer', customer_name)
    customer_address = frappe.get_doc('Address', doc.customer_address)
    buyer = Buyer(customer_name, customer_address.pincode, customer_address.city, customer_address.address_line1)
    buyer.tax_number = customer.tax_id
    buyer.tax_payer = TaxPayerConstant.TAXPAYER_HAS_TAXNUMBER
    invoice.buyer = buyer

    for item in doc.items:
        tax = ast.literal_eval(item.item_tax_rate)
        tax_rate = tax['VAT - PS']
        invoice_item = InvoiceItem(item.item_name, item.net_rate, item.stock_qty, item.stock_uom, str(tax_rate))
        invoice_item.net_price = item.net_amount
        invoice_item.vat_amount = item.net_amount * (tax_rate / 100)
        invoice_item.gross_amount = invoice_item.net_price + invoice_item.vat_amount
        invoice.add_item(invoice_item)

    result = agent.generate_invoice(invoice)
