import frappe
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.seller import Seller


class SellerHelper:
    @staticmethod
    def get_from_sales_invoice(sales_invoice):
        company_name = sales_invoice.company
        account = SellerHelper.get_account_or_default(company_name)
        seller = Seller(account['bank'], account['account_no'])
        return seller

    @staticmethod
    def get_account_or_default(company_name):
        company = frappe.get_doc('Company', company_name)
        bank_accounts = frappe.get_all('Bank Account', filters={'account': company.default_bank_account})
        account = {'bank': "", 'account_no': ""}
        if bank_accounts:
            bank_account = frappe.get_doc('Bank Account', bank_accounts[0])
            if bank_account:
                account['bank'] = bank_account.bank
                account['account_no'] = bank_account.bank_account_no
        return account
