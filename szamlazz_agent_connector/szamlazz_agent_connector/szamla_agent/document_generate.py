from functools import singledispatch

from szamlazz_agent_connector.szamlazz_agent_connector.helper.agent.szamla_agent_request_helper import \
    SzamlaAgentRequestHelper
from szamlazz_agent_connector.szamlazz_agent_connector.model.document.invoice.invoice import Invoice
from szamlazz_agent_connector.szamlazz_agent_connector.model.document.invoice.reverse_invoice import ReverseInvoice
from szamlazz_agent_connector.szamlazz_agent_connector.service.request_sender import RequestSender


@singledispatch
def document_generate(entity):
    raise ValueError(f"Not found any matching type for {entity}")


@document_generate.register
def _(entity: Invoice):
    request = SzamlaAgentRequestHelper.create('generateInvoice', entity)
    sender = RequestSender()
    sender.send(request)


@document_generate.register
def _(entity: ReverseInvoice):
    request = SzamlaAgentRequestHelper.create('generateReverseInvoice', entity)
    sender = RequestSender()
    sender.send(request)

