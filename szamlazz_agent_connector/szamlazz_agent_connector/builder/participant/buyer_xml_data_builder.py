from collections import OrderedDict

from szamlazz_agent_connector.szamlazz_agent_connector.model.participant.buyer import Buyer
from szamlazz_agent_connector.szamlazz_agent_connector.model.constant.xml_schema import XmlSchema
from szamlazz_agent_connector.szamlazz_agent_connector.model.exception.szamla_agent_exception import \
    SzamlaAgentException
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.szamla_agent_request import SzamlaAgentRequest
from szamlazz_agent_connector.szamlazz_agent_connector.validator.participant.buyer_validator import BuyerValidator


class BuyerXmlDataBuilder:
    def __init__(self):
        self._validator = BuyerValidator()

    def build_xml_data(self, request: SzamlaAgentRequest, buyer: Buyer):
        self._validator.check_fields(buyer)
        request_name = request.entity.xml_name
        if request_name == XmlSchema.XML_SCHEMA_CREATE_INVOICE:

            data = OrderedDict([
                ('nev', buyer.name),
                ('orszag', buyer.country),
                ('irsz', buyer.zip_code),
                ('telepules', buyer.city),
                ('cim', buyer.address)
            ])

            if buyer.email:
                data['email'] = buyer.email
            if buyer.send_email:
                data['sendEmail'] = buyer.send_email
            if buyer.tax_payer:
                data['adoalany'] = buyer.tax_payer
            if buyer.tax_number:
                data['adoszam'] = buyer.tax_number
            if buyer.tax_number_EU:
                data['adoszamEU'] = buyer.tax_number_EU
            if buyer.postal_name:
                data['postazasiNev'] = buyer.postal_name
            if buyer.postal_country:
                data['postazasiOrszag'] = buyer.postal_country
            if buyer.postal_zip:
                data['postazasiIrsz'] = buyer.postal_zip
            if buyer.postal_city:
                data['postazasiTelepules'] = buyer.postal_city
            if buyer.postal_address:
                data['postazasiCim'] = buyer.postal_address
            if buyer.ledger_data:
                data['vevokonyv'] = buyer.ledger_data.get_xml_data
            if buyer.id:
                data['azonosito'] = buyer.id
            if buyer.signatory_name:
                data['alairoNeve'] = buyer.signatory_name
            if buyer.phone:
                data['telefonszam'] = buyer.phone
            if buyer.comment:
                data['megjegyzes'] = buyer.comment

        elif request_name == XmlSchema.XML_SCHEMA_CREATE_REVERSE_INVOICE:
            data = OrderedDict()
            if buyer.email:
                data['email'] = buyer.email
            if buyer.tax_number:
                data['adoszam'] = buyer.tax_number
            if buyer.tax_number_EU:
                data['adoszamEU'] = buyer.tax_number_EU

        else:
            raise SzamlaAgentException(f"Not existing XML schema: {request_name}")

        return data
