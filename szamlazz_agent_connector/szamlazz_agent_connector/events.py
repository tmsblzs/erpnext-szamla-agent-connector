from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.buyer import Buyer
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.constant.document_constant import DocumentConstant
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.constant.invoice_constant import InvoiceConstant
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.constant.response_constant import ResponseConstant
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.constant.tax_payer_constant import TaxPayerConstant
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.document.invoice.invoice import Invoice
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.item.invoice_item import InvoiceItem
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.seller import Seller
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.szamla_agent_api import SzamlaAgentApi


def on_submit(doc, event_name):
    agent = SzamlaAgentApi.create('fzz87q95czd5fzz87qbkrwpcfzz87qd88fz8fzz87q')
    # agent.setting.response_type = ResponseConstant.RESULT_AS_XML

    invoice = Invoice(InvoiceConstant.INVOICE_TYPE_P_INVOICE)

    header = invoice.header
    header.payment_method = DocumentConstant.PAYMENT_METHOD_TRANSFER
    header.fulfillment = '2021-11-14'
    header.payment_due = '2021-11-30'
    header.prefix = ''
    header.preview_pdf = False
    header.invoice_template = InvoiceConstant.INVOICE_TEMPLATE_DEFAULT

    seller = Seller('OTP', '11738008-20850223')
    invoice.seller = seller

    buyer = Buyer('Kovacs Bt', '2030', 'Erd', 'Tarnoki utca 23')
    buyer.tax_number = '11111111-1-11'
    buyer.tax_payer = TaxPayerConstant.TAXPAYER_HAS_TAXNUMBER
    invoice.buyer = buyer

    item = InvoiceItem('Test item 1', 100, 2.0, 'db', '20')
    item.net_price = 200
    item.vat_amount = 40
    item.gross_amount = 240
    invoice.add_item(item)

    result = agent.generate_invoice(invoice)
