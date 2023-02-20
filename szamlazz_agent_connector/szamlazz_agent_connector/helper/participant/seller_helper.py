import frappe
from szamlazz_agent_connector.szamlazz_agent_connector.helper.account_helper import AccountHelper
from szamlazz_agent_connector.szamlazz_agent_connector.model.participant.seller import Seller


class SellerHelper:
    @staticmethod
    def get_from_sales_invoice(sales_invoice):
        company_name = sales_invoice.company
        company = frappe.get_doc('Company', company_name)
        account = AccountHelper.get_account_or_default(company)
        seller = Seller(account['bank'], account['account_no'])
        return seller

