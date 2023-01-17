import frappe
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.constant.document_constant import DocumentConstant
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.constant.invoice_constant import InvoiceConstant


class InvoiceHeaderHelper:

    @classmethod
    def fill_from_sales_invoice(cls, header, sales_invoice):
        header.payment_method = cls.get_payment_method(sales_invoice.payment_terms_template)
        header.fulfillment = sales_invoice.fulfillment_date
        header.payment_due = sales_invoice.due_date
        header.prefix = ''
        header.preview_pdf = False
        header.invoice_template = InvoiceConstant.INVOICE_TEMPLATE_DEFAULT
        return header

    @classmethod
    def get_payment_method(cls, payment_terms_template_name):
        terms = frappe.get_all("Payment Terms Template Detail",
                               filters={'payment_term': payment_terms_template_name},
                               fields=['name'])
        if terms:
            term = frappe.get_doc("Payment Terms Template Detail", terms[0].name)
            return cls.get_payment_mode(term.mode_of_payment)

    @staticmethod
    def get_payment_mode(mode_of_payment):
        agent_mode_of_payment = frappe.get_all('SzamlazzAgentConnectorModeOfPayments',
                                               filters={'mode_of_payment_name': mode_of_payment})
        if agent_mode_of_payment:
            agent_payment_method_type = frappe.get_doc('SzamlazzAgentConnectorModeOfPayments', agent_mode_of_payment[0])
            if agent_payment_method_type:
                return agent_payment_method_type.agent_payment_method_type
        return DocumentConstant.PAYMENT_METHOD_CASH
