import frappe


class AccountHelper:
    @staticmethod
    def get_account_or_default(company):
        bank_accounts = frappe.get_all('Bank Account', filters={'account': company.default_bank_account})
        account = {'bank': "", 'account_no': ""}
        if bank_accounts:
            bank_account = frappe.get_doc('Bank Account', bank_accounts[0])
            if bank_account:
                account['bank'] = bank_account.bank
                account['account_no'] = bank_account.bank_account_no
        return account
