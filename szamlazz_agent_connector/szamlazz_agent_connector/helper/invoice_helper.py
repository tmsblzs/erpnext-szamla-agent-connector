from szamlazz_agent_connector.szamlazz_agent_connector.helper.buyer_helper import BuyerHelper
from szamlazz_agent_connector.szamlazz_agent_connector.helper.invoice_header_helper import InvoiceHeaderHelper
from szamlazz_agent_connector.szamlazz_agent_connector.helper.sales_items_helper import SalesItemsHelper
from szamlazz_agent_connector.szamlazz_agent_connector.helper.seller_helper import SellerHelper
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.constant.invoice_constant import InvoiceConstant
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.document.invoice.invoice import Invoice


class InvoiceHelper:
    @staticmethod
    def create_from_sales_invoice(sales_invoice):
        invoice = Invoice(InvoiceConstant.INVOICE_TYPE_P_INVOICE)
        InvoiceHeaderHelper.fill_from_sales_invoice(invoice.header, sales_invoice)
        invoice.seller = SellerHelper.get_from_sales_invoice(sales_invoice)
        invoice.buyer = BuyerHelper.get_buyer_from_sales_invoice(sales_invoice)
        SalesItemsHelper.add_items_to_invoice(invoice, sales_invoice, sales_invoice.tax_category)
        return invoice

