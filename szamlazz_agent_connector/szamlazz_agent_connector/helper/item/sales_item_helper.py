import frappe
from szamlazz_agent_connector.szamlazz_agent_connector.helper.participant.tax_helper import TaxHelper
from szamlazz_agent_connector.szamlazz_agent_connector.mapper.item.invoice_item_mapper import InvoiceItemMapper


class SalesItemHelper:
    @staticmethod
    def get_item_from_sales_invoice_item(sales_invoice_item, tax_category):
        stock_item = frappe.get_doc("Item", sales_invoice_item.item_code)
        tax_rate = TaxHelper.get_tax_rate_from_stock_item_by_tax_category(stock_item, tax_category)
        invoice_item = InvoiceItemMapper.from_sales_invoice_item(sales_invoice_item, tax_rate)
        return invoice_item

