from functools import singledispatch

from numpy import iterable

from szamlazz_agent_connector.szamlazz_agent_connector.builder.participant.buyer_xml_data_builder import BuyerXmlDataBuilder
from szamlazz_agent_connector.szamlazz_agent_connector.builder.document.invoice.invoice_xml_data_builder import \
    InvoiceXmlDataBuilder
from szamlazz_agent_connector.szamlazz_agent_connector.builder.header.invoice_header_xml_data_builder import \
    InvoiceHeaderXmlDataBuilder
from szamlazz_agent_connector.szamlazz_agent_connector.builder.item.invoice_item_xml_data_builder import \
    InvoiceItemXmlDataBuilder
from szamlazz_agent_connector.szamlazz_agent_connector.builder.item.invoice_items_xml_data_builder import \
    InvoiceItemsXmlDataBuilder
from szamlazz_agent_connector.szamlazz_agent_connector.builder.participant.seller_xml_data_builder import SellerXmlDataBuilder
from szamlazz_agent_connector.szamlazz_agent_connector.builder.agent.setting_xml_data_builder import SettingXmlDataBuilder
from szamlazz_agent_connector.szamlazz_agent_connector.builder.participant.taxpayer_xml_data_builder import TaxpayerXmlDataBuilder
from szamlazz_agent_connector.szamlazz_agent_connector.model.participant.buyer import Buyer
from szamlazz_agent_connector.szamlazz_agent_connector.model.document.invoice.invoice import Invoice
from szamlazz_agent_connector.szamlazz_agent_connector.model.header.reverse_invoice_header import \
    ReverseInvoiceHeader
from szamlazz_agent_connector.szamlazz_agent_connector.model.item.invoice_item import InvoiceItem
from szamlazz_agent_connector.szamlazz_agent_connector.model.participant.seller import Seller
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.szamla_agent_setting import SzamlaAgentSetting
from szamlazz_agent_connector.szamlazz_agent_connector.model.participant.taxpayer import Taxpayer


@singledispatch
def build_xml_data(model, request):
    raise ValueError(f"No xml data builder found for {model}!")
    pass


@build_xml_data.register
def _(model: Invoice, request):
    return InvoiceXmlDataBuilder().build_xml_data(request, model)


@build_xml_data.register
def _(model: ReverseInvoiceHeader, request):
    return InvoiceHeaderXmlDataBuilder().build_xml_data(request, model)


@build_xml_data.register
def _(model: Seller, request):
    return SellerXmlDataBuilder().build_xml_data(request, model)


@build_xml_data.register
def _(model: Buyer, request):
    return BuyerXmlDataBuilder().build_xml_data(request, model)


@build_xml_data.register
def _(model: Taxpayer, request):
    return TaxpayerXmlDataBuilder(SettingXmlDataBuilder()).build_xml_data(request, model)


@build_xml_data.register
def _(model: SzamlaAgentSetting, request):
    return SettingXmlDataBuilder().build_xml_data(request, model)


@build_xml_data.register
def _(model: InvoiceItem, request):
    return InvoiceItemXmlDataBuilder().build_xml_data(model)


# @build_xml_data.register(iterable(InvoiceItem))
# def _(model, request):
#     return InvoiceItemsXmlDataBuilder().build_xml_data(request, model)


