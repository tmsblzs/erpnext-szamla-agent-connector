from collections import OrderedDict

from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.constant.xml_schema import XmlSchema
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.exception.szamla_agent_exception import \
    SzamlaAgentException
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.seller import Seller
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.szamla_agent_request import SzamlaAgentRequest
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.szamla_agent_util import SzamlaAgentUtil


class SellerXmlDataBuilder:
    def build_xml_data(self, request: SzamlaAgentRequest, seller: Seller):
        request_name = request.xml_name

        if request_name == XmlSchema.XML_SCHEMA_CREATE_INVOICE:
            data = OrderedDict()

            if seller.bank:
                data['bank'] = seller.bank
            if seller.bank_account:
                data['bankszamlaszam'] = seller.bank_account
            if seller.signatory_name:
                data['alaironeve'] = seller.signatory_name

            email_data = self._get_xml_email_data()
            if email_data:
                data.update(email_data)
        elif request_name == XmlSchema.XML_SCHEMA_CREATE_REVERSE_INVOICE:
            data = self._get_xml_email_data(seller)
        else:
            raise SzamlaAgentException(SzamlaAgentException.XML_SCHEMA_TYPE_NOT_EXISTS + f": {request_name}")
        return data

    def _get_xml_email_data(self, seller: Seller):
        data = OrderedDict()

        if seller.email_reply_to:
            data['emailReplyto'] = seller.email_reply_to
        if seller.email_subject:
            data['emailTargy'] = seller.email_subject
        if seller.email_content:
            data['emailSzoveg'] = seller.email_content

        return data
