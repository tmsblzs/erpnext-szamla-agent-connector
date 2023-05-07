import json
import logging
import xml.etree.ElementTree as Et
from base64 import b64encode

import xmldict as xmldict

from szamlazz_agent_connector.szamlazz_agent_connector.model.constant.agent_constant import AgentConstant
from szamlazz_agent_connector.szamlazz_agent_connector.model.constant.document_constant import DocumentConstant
from szamlazz_agent_connector.szamlazz_agent_connector.model.constant.response_constant import ResponseConstant
from szamlazz_agent_connector.szamlazz_agent_connector.model.constant.xml_schema import XmlSchema
from szamlazz_agent_connector.szamlazz_agent_connector.model.exception.szamla_agent_exception import \
    SzamlaAgentException
from szamlazz_agent_connector.szamlazz_agent_connector.model.response.invoice_response import InvoiceResponse
from szamlazz_agent_connector.szamlazz_agent_connector.model.szamla_agent_util import SzamlaAgentUtil


class SzamlaAgentResponse:

    @property
    def agent(self):
        return self._agent

    def __init__(self, request, response):
        self._agent = request.agent
        self._request = request
        self.document_number = None
        self.xml_data = None
        self.http_code = None
        self.content = None
        self.response = response
        self.xml_schema_type = response['headers']['schema-type']

    def handle_response(self):
        response = self.response
        agent = self._agent
        invoice_response = InvoiceResponse()

        if response['headers'] and len(response['headers']) > 0:
            headers = response['headers']

            if 'szlahu_down' in headers and headers['szlahu_down']:
                raise SzamlaAgentException(SzamlaAgentException.SYSTEM_DOWN)
        else:
            raise SzamlaAgentException(SzamlaAgentException.AGENT_RESPONSE_NO_HEADER)

        if 'http_code' in headers:
            self.http_code = headers['http_code']

        if self.is_xml_response():
            self.build_response_xml_data(invoice_response)
        else:
            self.build_response_text_data(invoice_response)

        self.build_response_obj_data(invoice_response)
        # self.create_xml_file(self.xml_data, invoice_response)
        self.check_fields()

        if self.has_invoice_notification_send_error(invoice_response):
            agent.write_log(SzamlaAgentException.INVOICE_NOTIFICATION_SEND_FAILED, )

        if invoice_response.is_failed():
            raise SzamlaAgentException(SzamlaAgentException.AGENT_ERROR +
                                       f"[{invoice_response.error_code}], {invoice_response.error_message}")
        elif invoice_response.is_success():
            agent.write_log("Agent calling is successfully ended.", logging.DEBUG)
            if self.is_not_tax_payer_xml_response():
                try:
                    if agent.download_pdf:
                        pdf_data = self.response['body']
                        xml_name = self._request.entity.xml_name
                        if not pdf_data and xml_name != XmlSchema.XML_SCHEMA_SEND_RECEIPT \
                                and xml_name != XmlSchema.XML_SCHEMA_PAY_INVOICE:
                            raise SzamlaAgentException(SzamlaAgentException.DOCUMENT_DATA_IS_MISSING)
                        elif pdf_data:
                            invoice_response.pdf_file = pdf_data

                            if agent.pdf_file_save:
                                with open(self.get_pdf_file_name(invoice_response), 'wb') as f:
                                    f.write(pdf_data)
                    else:
                        self.content = response['body']
                except Exception as ex:
                    agent.write_log(SzamlaAgentException.PDF_FILE_SAVE_FAILED +
                                    f": {ex.with_traceback(None)}", logging.DEBUG)
                    raise ex
        return invoice_response

    def check_fields(self):
        response = self.response
        if self.is_agent_invoice_response():
            for header in response['headers']:
                if header.startswith('szlahu_'):
                    return
            raise SzamlaAgentException(SzamlaAgentException.NO_SZLAHU_KEY_IN_HEADER)

    def create_xml_file(self, xml_data, invoice_response):
        agent = self.agent
        if self.is_tax_payer_xml_response():
            response = self.response
            xml = Et.fromstring(response['body'])
        else:
            xml = Et.fromstring(xml_data)

        name = ''
        if invoice_response.is_failed():
            name = 'error-'
        name += agent.request.xml_name.lower()

        response_type = agent.response_type
        if response_type == ResponseConstant.RESULT_AS_XML or response_type == ResponseConstant.RESULT_AS_TAXPAYER_XML:
            name += '-xml'
        elif response_type == ResponseConstant.RESULT_AS_TEXT:
            name += "-text"
        else:
            raise SzamlaAgentException(SzamlaAgentException.RESPONSE_TYPE_NOT_EXISTS + f"{response_type}")

        file_name = SzamlaAgentUtil.get_xml_file_name('response', name, agent.request.entity)
        et = Et.ElementTree(xml)
        et.write(file_name,
                 xml_declaration=True,
                 encoding="utf-8",
                 method='xml')

        agent.write_log("XML file saving is succeeded." + SzamlaAgentUtil.get_real_path(file_name), logging.DEBUG)

    def get_pdf_file_name(self, invoice_response, with_path=True):
        header = self._request.get_entity_header()
        from szamlazz_agent_connector.szamlazz_agent_connector.model.header.invoice_header import InvoiceHeader
        if isinstance(header, InvoiceHeader) and header.preview_pdf:
            entity = self._agent.get_request_entity()

            name = ''
            from szamlazz_agent_connector.szamlazz_agent_connector.model.document.invoice.invoice import Invoice
            if entity and isinstance(entity, Invoice):
                name += entity.__class__.__name__
            document_number = f"{name.lower()}preview-{SzamlaAgentUtil.get_date_time_with_milliseconds()}"
        else:
            document_number = invoice_response.document_number

        if with_path:
            filename = SzamlaAgentResponse.get_pdf_file_abs_path(f'{document_number}.pdf')
        else:
            filename = f"{document_number}.pdf"
        return filename

    @staticmethod
    def get_pdf_file_abs_path(pdf_file_name):
        return SzamlaAgentUtil.get_abs_path(AgentConstant.PDF_FILE_SAVE_PATH, pdf_file_name)

    def download_pdf(self):
        pdf_file_name = self.get_pdf_file_name(False)

        if pdf_file_name:
            print("Content-type:application/pdf")
            print(f"Content-Disposition:attachment;filename={pdf_file_name}.pdf")
            with(f"{pdf_file_name}.pdf", 'o') as file:
                for line in file:
                    print(line)
            return True
        return False

    def is_agent_invoice_text_response(self):
        return self.is_agent_invoice_response() and self.agent.response_type == ResponseConstant.RESULT_AS_TEXT

    def is_agent_invoice_xml_response(self):
        return self.is_agent_invoice_response() and self.agent.response_type == ResponseConstant.RESULT_AS_XML

    def is_agent_receipt_text_response(self):
        return self.is_agent_receipt_response() and self.agent.response_type == ResponseConstant.RESULT_AS_TEXT

    def is_agent_receipt_xml_response(self):
        return self.is_agent_receipt_response() and self.agent.response_type == ResponseConstant.RESULT_AS_XML

    def is_tax_payer_xml_response(self):
        result = True
        if self.xml_schema_type != 'taxpayer':
            return False

        if self.agent.response_type != ResponseConstant.RESULT_AS_TAXPAYER_XML:
            result = False
        return result

    def is_not_tax_payer_xml_response(self):
        return not self.is_tax_payer_xml_response()

    def is_xml_response(self):
        return self.is_agent_invoice_xml_response() or self.is_agent_receipt_xml_response() \
               or self.is_tax_payer_xml_response()

    def is_agent_invoice_response(self):
        return self.xml_schema_type == DocumentConstant.DOCUMENT_TYPE_INVOICE

    def is_agent_proforma_response(self):
        return self.xml_schema_type == DocumentConstant.DOCUMENT_TYPE_PROFORMA

    def is_agent_receipt_response(self):
        return self.xml_schema_type == DocumentConstant.DOCUMENT_TYPE_RECEIPT

    def build_response_text_data(self, invoice_response):
        response = self.response
        xml_data = Et.Element('response')
        headers = Et.SubElement(xml_data, 'headers')
        for header in response['headers']:
            header_item = Et.SubElement(headers, header)
            header_item.text = response['headers'][header]

        if self.is_agent_receipt_response():
            content = b64encode(response['body']).decode('utf-8')
        else:
            if self.agent.download_pdf:
                content = b64encode(response['body']).decode('utf-8')
            else:
                content = response['body']
        body = Et.SubElement(xml_data, 'body')
        body.text = content

        self.xml_data = '<?xml version="1.0" encoding="utf-8" ?>' + Et.tostring(xml_data).decode('utf-8')

    def build_response_xml_data(self, invoice_response):
        response = self.response
        if self.is_tax_payer_xml_response:
            xml_data = Et.parse(response['body'])
        else:
            xml_data = Et.parse(response['body'])
            headers = Et.SubElement(xml_data.getroot(), 'headers')
            for header in response['headers']:
                Et.SubElement(headers, header, response['headers'][header])
        self.xml_data = xml_data

    def to_xml(self):
        if self.xml_data:
            return self.xml_data
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

    def get_response_data(self):
        result = {}
        if self.is_not_tax_payer_xml_response():
            result['documentNumber'] = self.document_number

        if self.xml_data:
            result['result'] = xmldict.xml_to_dict(self.xml_data)
        else:
            result['result'] = self.content

        return result

    def build_response_obj_data(self, invoice_response):
        obj = None
        response_type = self.agent.response_type
        json_array = self.to_array()

        if 'result' not in json_array:
            raise SzamlaAgentException()

        result = json_array['result']
        if 'response' not in result:
            raise SzamlaAgentException

        if self.is_agent_invoice_response():
            from szamlazz_agent_connector.szamlazz_agent_connector.parser.document.invoice_parser import InvoiceParser
            InvoiceParser.parse_data(result['response'], invoice_response, response_type)

    def has_invoice_notification_send_error(self, invoice_response):
        if self.is_agent_invoice_response() and invoice_response.has_invoice_notification_send_error():
            return True
        return False
