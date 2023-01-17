from collections import OrderedDict

from szamlazz_agent_connector.szamlazz_agent_connector.model.constant.xml_schema import XmlSchema
from szamlazz_agent_connector.szamlazz_agent_connector.model.exception.szamla_agent_exception import \
    SzamlaAgentException
from szamlazz_agent_connector.szamlazz_agent_connector.model.participant.seller import Seller
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.szamla_agent_request import SzamlaAgentRequest
from szamlazz_agent_connector.szamlazz_agent_connector.validator.participant.seller_validator import SellerValidator


class SellerXmlDataBuilder:
    def __init__(self, validator: SellerValidator):
        self._validator = validator

    def build_xml_data(self, request: SzamlaAgentRequest, seller: Seller):
        self._validator.check_fields(seller)

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
