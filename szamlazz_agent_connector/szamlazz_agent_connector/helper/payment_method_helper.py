import frappe
from szamlazz_agent_connector.szamlazz_agent_connector.helper.payment_mode_helper import PaymentModeHelper
from szamlazz_agent_connector.szamlazz_agent_connector.model.constant.document_constant import DocumentConstant


class PaymentMethodHelper:
    @staticmethod
    def get_payment_method(payment_terms_template_name):
        terms = frappe.get_all("Payment Terms Template Detail",
                               filters={'payment_term': payment_terms_template_name},
                               fields=['name'])
        if terms:
            term = frappe.get_doc("Payment Terms Template Detail", terms[0].name)
            return PaymentModeHelper.get_payment_mode(term.mode_of_payment)
        return DocumentConstant.PAYMENT_METHOD_CASH
