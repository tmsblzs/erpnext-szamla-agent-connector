from szamlazz_agent_connector.szamlazz_agent_connector.helper.item.sales_item_helper import SalesItemHelper


class SalesItemsHelper:
    @staticmethod
    def add_items_to_invoice(invoice, sales_invoice_items, tax_category):
        for item in sales_invoice_items:
            invoice_item = SalesItemHelper.get_item_from_sales_invoice_item(item, tax_category)
            invoice.add_item(invoice_item)
