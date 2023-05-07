import frappe
from szamlazz_agent_connector.szamlazz_agent_connector.model.constant.document_constant import DocumentConstant


def after_install():
    insert_doc_payment_method_type(DocumentConstant.PAYMENT_METHOD_PAYPAL)
    insert_doc_payment_method_type(DocumentConstant.PAYMENT_METHOD_TRANSFER)
    insert_doc_payment_method_type(DocumentConstant.PAYMENT_METHOD_CASH)
    insert_doc_payment_method_type(DocumentConstant.PAYMENT_METHOD_CHEQUE)
    insert_doc_payment_method_type(DocumentConstant.PAYMENT_METHOD_BANKCARD)
    insert_doc_payment_method_type(DocumentConstant.PAYMENT_METHOD_CASH_ON_DELIVERY)
    insert_doc_payment_method_type(DocumentConstant.PAYMENT_METHOD_OTP_SIMPLE)
    insert_doc_payment_method_type(DocumentConstant.PAYMENT_METHOD_SZEP_CARD)


def insert_doc_payment_method_type(name):
    doc = frappe.get_doc({
        "doctype": "SzamlazzAgentConnectorPaymentMethodType",
        "name": name,
        "label": name,
    })
    doc.flags.name_set = True
    doc.insert()

