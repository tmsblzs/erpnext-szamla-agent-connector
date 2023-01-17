from szamlazz_agent_connector.szamlazz_agent_connector.helper.participant.buyer_helper import BuyerHelper
from szamlazz_agent_connector.szamlazz_agent_connector.helper.header.invoice_header_helper import InvoiceHeaderHelper
from szamlazz_agent_connector.szamlazz_agent_connector.helper.item.sales_items_helper import SalesItemsHelper
from szamlazz_agent_connector.szamlazz_agent_connector.helper.participant.seller_helper import SellerHelper
from szamlazz_agent_connector.szamlazz_agent_connector.model.constant.invoice_constant import InvoiceConstant
from szamlazz_agent_connector.szamlazz_agent_connector.model.document.invoice.invoice import Invoice


class InvoiceHelper:
    @staticmethod
    def create_from_sales_invoice(sales_invoice):
        seller = SellerHelper.get_from_sales_invoice(sales_invoice)
        buyer = BuyerHelper.get_buyer_from_sales_invoice(sales_invoice)
        invoice = Invoice(
            seller,
            buyer,
            InvoiceConstant.INVOICE_TYPE_P_INVOICE)
        InvoiceHeaderHelper.fill_from_sales_invoice(invoice.header, sales_invoice)
        SalesItemsHelper.add_items_to_invoice(invoice, sales_invoice.items, sales_invoice.tax_category)
        return invoice

