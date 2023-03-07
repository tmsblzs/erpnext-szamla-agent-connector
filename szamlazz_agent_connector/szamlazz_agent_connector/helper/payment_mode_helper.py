import frappe
from szamlazz_agent_connector.szamlazz_agent_connector.model.constant.document_constant import DocumentConstant


class PaymentModeHelper:
    @staticmethod
    def get_payment_mode(mode_of_payment):
        agent_mode_of_payment = frappe.get_all('SzamlazzAgentConnectorModeOfPayments',
                                               filters={'mode_of_payment_name': mode_of_payment})
        if agent_mode_of_payment:
            agent_payment_method_type = frappe.get_doc('SzamlazzAgentConnectorModeOfPayments', agent_mode_of_payment[0])
            if agent_payment_method_type:
                return agent_payment_method_type.agent_payment_method_type
        return DocumentConstant.PAYMENT_METHOD_CASH
