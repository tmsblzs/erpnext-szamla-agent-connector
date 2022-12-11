import os

import dateutil

import frappe


class AgentInvoiceHelper:
    @staticmethod
    def create_and_insert_from_sales_invoice(sales_invoice, pdf_file_name, result_file_name):
        agent_invoice = frappe.new_doc("SzamlazzAgentConnectorInvoice")
        agent_invoice.buyer = sales_invoice.customer
        agent_invoice.created_at = dateutil.utils.today()
        agent_invoice.pdf_file = pdf_file_name
        agent_invoice.invoice_date = sales_invoice.posting_date
        agent_invoice.sum = sales_invoice.base_net_total
        agent_invoice.is_successfully_send = True
        agent_invoice.own_invoice_number = sales_invoice.name
        agent_invoice.szamlazz_invoice_number = os.path.splitext(result_file_name)[0]
        agent_invoice.sales_invoice = sales_invoice.name
        agent_invoice.insert()
        return agent_invoice

    @staticmethod
    def get_by_own_invoice_number(own_invoice_number):
        agent_invoice = frappe.get_all('SzamlazzAgentConnectorInvoice', filters={'own_invoice_number': own_invoice_number})
        if not agent_invoice:
            raise TypeError("Szamlazz Agent Invoice not found!")
        return agent_invoice

    @staticmethod
    def get_by_name(agent_invoice):
        invoice = frappe.get_doc("SzamlazzAgentConnectorInvoice", agent_invoice)
        if not invoice:
            raise TypeError("Invoice not found!")

