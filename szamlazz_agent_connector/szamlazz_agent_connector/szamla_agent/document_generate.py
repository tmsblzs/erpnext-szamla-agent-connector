from functools import singledispatch

from szamlazz_agent_connector.szamlazz_agent_connector.helper.agent.szamla_agent_request_helper import \
    SzamlaAgentRequestHelper
from szamlazz_agent_connector.szamlazz_agent_connector.model.document.invoice.invoice import Invoice
from szamlazz_agent_connector.szamlazz_agent_connector.model.document.invoice.reverse_invoice import ReverseInvoice
from szamlazz_agent_connector.szamlazz_agent_connector.service.request_sender import RequestSender
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.szamla_agent_request_type import \
    SzamlaAgentRequestType


@singledispatch
def document_generate(entity):
    raise ValueError(f"Not found any matching type for {entity}")


@document_generate.register
def _(entity: Invoice):
    request = SzamlaAgentRequestHelper.create(SzamlaAgentRequestType.INVOICE, entity)
    sender = RequestSender()
    response = sender.send(request)
    return request, response


@document_generate.register
def _(entity: ReverseInvoice):
    request = SzamlaAgentRequestHelper.create(SzamlaAgentRequestType.REVERSE_INVOICE, entity)
    sender = RequestSender()
    response = sender.send(request)
    return request, response

