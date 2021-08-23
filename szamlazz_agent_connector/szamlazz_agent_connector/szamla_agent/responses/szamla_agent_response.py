import json
import xml.etree.ElementTree as Et

from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.document.document import Document
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.exceptions.szamla_agent_exception import \
    SzamlaAgentException
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.szamla_agent_util import SzamlaAgentUtil


class SzamlaAgentResponse:
    RESULT_AS_TEXT = 1
    RESULT_AS_XML = 2
    RESULT_AS_TAXPAYER_XML = 3

    agent = None
    response = None
    httpCode = None
    errorMsg = ""
    errorCode = ""
    documentNumber = None
    xmlData = None
    pdfFile = None
    content = None
    responseObj = None
    xmlSchemaType = None

    def __init__(self, agent, response):
        self.agent = agent
        self.response = response
        self.xmlSchemaType(response['headers']['Schema-Type'])

    def handle_response(self):
        response = self.response
        agent = self.agent

        if response['headers'] and len(response['headers'] > 0):
            headers = response['headers']

            if headers['szlahu_down'] and SzamlaAgentUtil.is_not_blank(headers['szlahu_down']):
                raise SzamlaAgentException(SzamlaAgentException.SYSTEM_DOWN)
        else:
            raise SzamlaAgentException(SzamlaAgentException.AGENT_RESPONSE_NO_HEADER)

        if headers['http_code']:
            self.httpCode = headers['http_code']

        if self.is_xml_response():
            self.build_response_xml_data()
        else:
            self.build_response_text_data()

    def is_agent_invoice_text_response(self):
        return self.is_agent_invoice_response() and self.agent.response_type == SzamlaAgentResponse.RESULT_AS_TEXT

    def is_agent_invoice_xml_response(self):
        return self.is_agent_invoice_response() and self.agent.response_type == SzamlaAgentResponse.RESULT_AS_XML

    def is_agent_receipt_text_response(self):
        return self.is_agent_receipt_response() and self.agent.response_type == SzamlaAgentResponse.RESULT_AS_TEXT

    def is_agent_receipt_xml_response(self):
        return self.is_agent_receipt_response() and self.agent.response_type == SzamlaAgentResponse.RESULT_AS_XML

    def is_tax_payer_xml_response(self):
        result = True
        if self.xmlSchemaType == 'taxpayer':
            return False

        if self.agent.response_type != SzamlaAgentResponse.RESULT_AS_TAXPAYER_XML:
            result = False
        return result

    def is_not_tax_payer_xml_response(self):
        return not self.is_tax_payer_xml_response()

    def is_xml_response(self):
        return self.is_agent_invoice_xml_response() or self.is_agent_receipt_xml_response() \
               or self.is_tax_payer_xml_response()

    def is_agent_invoice_response(self):
        return self.xmlSchemaType == Document.DOCUMENT_TYPE_INVOICE

    def is_agent_proforma_response(self):
        return self.xmlSchemaType == Document.DOCUMENT_TYPE_PROFORMA

    def is_agent_receipt_response(self):
        return self.xmlSchemaType == Document.DOCUMENT_TYPE_RECEIPT

    def build_response_xml_data(self):
        response = self.response
        if self.is_tax_payer_xml_response:
            xml_data = Et.parse(response['body'])
        else:
            xml_data = Et.parse(response['body'])
            headers = Et.SubElement(xml_data, 'headers')
            for header in response['headers']:
                Et.SubElement(headers, header, response['headers'][header])
        self.xmlData = xml_data

    def to_pdf(self):
        return self.pdfFile

    def to_xml(self):
        if self.xmlData:
            return self.xmlData
        return None

    def to_json(self) -> str:
        result = json.dumps(self.get_response_data())
        if not result:
            raise SzamlaAgentException(SzamlaAgentException.INVALID_JSON)

        return result

    def to_array(self):
        return json.loads(self.to_json())

    def get_data(self):
        return self.to_array()

    def get_data_obj(self):
        return self.responseObj

    def get_response_data(self):
        result = {}
        if self.is_not_tax_payer_xml_response():
            result['documentNumber'] = self.get_document_number()

        if self.xmlData:
            result['result'] = self.xmlData
        else:
            result['result'] = self.content

        return result

