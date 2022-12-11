import frappe
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.seller import Seller


class SellerHelper:
    @staticmethod
    def get_from_sales_invoice(sales_invoice):
        company_name = sales_invoice.company
        company = frappe.get_doc('Company', company_name)
        bank_accounts = frappe.get_all('Bank Account', filters={'account': company.default_bank_account})
        bank_account = frappe.get_doc('Bank Account', bank_accounts[0])
        seller = Seller(bank_account.bank, bank_account.bank_account_no)
        return seller
