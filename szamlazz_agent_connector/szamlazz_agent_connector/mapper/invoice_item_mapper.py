from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.item.invoice_item import InvoiceItem


class InvoiceItemMapper:
    @staticmethod
    def from_sales_invoice_item(sales_invoice_item, tax_rate):
        invoice_item = InvoiceItem(sales_invoice_item.item_name, sales_invoice_item.net_rate, sales_invoice_item.stock_qty, sales_invoice_item.stock_uom, str(tax_rate))
        invoice_item.net_price = sales_invoice_item.net_amount
        invoice_item.vat_amount = sales_invoice_item.net_amount * (tax_rate / 100)
        invoice_item.gross_amount = invoice_item.net_price + invoice_item.vat_amount
        return invoice_item
