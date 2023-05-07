import frappe


class TaxHelper:
    @staticmethod
    def get_tax_rate_from_stock_item_by_tax_category(stock_item, tax_category):
        tax = [x for x in stock_item.taxes if x.tax_category == tax_category]
        tax_rate = 0
        if tax:
            tax_template = frappe.get_doc("Item Tax Template", tax[0].item_tax_template)
            if len(tax_template.taxes) > 0:
                tax_rate = tax_template.taxes[0].tax_rate
        return tax_rate
