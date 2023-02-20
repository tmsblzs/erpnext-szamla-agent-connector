import frappe
from szamlazz_agent_connector.szamlazz_agent_connector.model.participant.buyer import Buyer
from szamlazz_agent_connector.szamlazz_agent_connector.model.constant.tax_payer_constant import TaxPayerConstant


class BuyerHelper:
    @staticmethod
    def get_buyer_from_sales_invoice(sales_invoice):
        customer_name = sales_invoice.customer
        customer = frappe.get_doc('Customer', customer_name)
        customer_address = frappe.get_doc('Address', sales_invoice.customer_address)
        buyer = Buyer(
            customer.customer_name,
            customer_address.pincode,
            customer_address.city,
            customer_address.address_line1)
        buyer.tax_number = customer.tax_id
        buyer.tax_payer = TaxPayerConstant.TAXPAYER_HAS_TAXNUMBER
        return buyer
