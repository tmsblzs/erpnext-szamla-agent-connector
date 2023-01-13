import fileinput
import html
import logging
import random
import re
from io import BytesIO

import mmap
import os

import xml.etree.ElementTree as ET
from urllib.parse import urlencode
from lxml import etree

import pycurl

from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.constant.agent_constant import AgentConstant
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.constant.document_constant import DocumentConstant
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.constant.xml_schema import XmlSchema
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.exception.szamla_agent_exception import \
    SzamlaAgentException
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.szamla_agent_util import SzamlaAgentUtil


class SzamlaAgentRequest:
    HTTP_OK = 200
    LF = "\n"
    CRLF = "\r\n"

    # Számla Agent XML séma alapértelmezett URL
    # (az XML generálásához használjuk, ne változtasd meg)
    XML_BASE_URL = 'http://www.szamlazz.hu/'

    # Számla Agent kérés maximális idő másodpercben
    REQUEST_TIMEOUT = 30

    # Számla Agent kérés módja: natív
    CALL_METHOD_LEGACY = 1

    # Számla Agent kérés módja: CURL
    CALL_METHOD_CURL = 2

    # Számla Agent kérés módja: automatikus
    CALL_METHOD_AUTO = 3

    # Kérés engedélyezési módok
    REQUEST_AUTHORIZATION_BASIC_AUTH = 1

    XMLNS_XSI_NAME = 'xmlns:xsi'
    XMLNS_XSI_URL = 'http://www.w3.org/2001/XMLSchema-instance'

    XSI_SCHEMA_LOCATION_NAME = 'xsi:schemaLocation'

    def __init__(self, agent, request_type, entity):
        self.agent = agent
        self.type = request_type
        self.entity = entity
        self.cData = True
        self.filename = ''
        self.xml_name = ''
        self.xsd_dir = ''
        self.xml_data = ''
        self.xml_file_path = ''
        self.delim = ''
        self.post_fields = ''
        self.response_headers = {}

    def build_xml_data(self):
        self.set_xml_file_data(self.type)
        agent = self.agent
        agent.write_log("Collecting XML data is starting", logging.DEBUG)
        xml_data = self.entity.build_xml_data(self)

        ET.register_namespace('', self.get_xml_ns())
        xml_node = ET.Element("{" + self.get_xml_ns() + "}" + self.xml_name,
                              **{SzamlaAgentRequest.XMLNS_XSI_NAME: SzamlaAgentRequest.XMLNS_XSI_URL},
                              **{SzamlaAgentRequest.XSI_SCHEMA_LOCATION_NAME : self.get_schema_location()})
        self.array_to_xml(xml_data, xml_node)
        try:
            et = ET.ElementTree(xml_node)
            f = BytesIO()
            et.write(f,
                     encoding='utf-8',
                     xml_declaration=False,
                     method='xml')
            xml_text = f.getvalue()
            f.close()
            # xml = etree.XML(xml_text, etree.XMLParser(remove_blank_text=True))
            # for parent in xml.xpath('//*[./*]'):
            #     parent[:] = sorted(parent, key=lambda x: x.tag)
            # xml_text = etree.tostring(xml, pretty_print=True)
            result = SzamlaAgentUtil.check_valid_xml(xml_text)
            if not result:
                raise SzamlaAgentException(
                    SzamlaAgentException.XML_NOT_VALID + f"in line {result[0].line}: {result[0].message}")
            self.xml_data = xml_text.replace(bytearray(SzamlaAgentRequest.LF, 'utf-8'), bytearray('', 'utf-8'))

            agent.write_log("Collection XML data has done.", logging.DEBUG)
            # et = ET.fromstring(xml_text)
            # self.create_xml_file(ET.ElementTree(et))
            self.create_xml_file(et)
        except Exception as ex:
            raise SzamlaAgentException(SzamlaAgentException.XML_DATA_BUILD_FAILED + format(ex))

    def array_to_xml(self, xml_data, xml_node):
        for key in xml_data:
            if isinstance(xml_data[key], dict):
                field_key = key
                if key.find("item") != -1:
                    field_key = 'tetel'
                if key.find("note") != -1:
                    field_key = 'kifizetes'
                sub_node = ET.SubElement(xml_node, "{" + self.get_xml_ns() + "}" + field_key)
                self.array_to_xml(xml_data[key], sub_node)
            else:
                if isinstance(xml_data[key], (int, float)):
                    value = str(xml_data[key]).lower()
                elif self.cData:
                    value = html.escape(xml_data[key])
                else:
                    value = 'true' if xml_data[key] else 'false'

                sub_element = ET.SubElement(xml_node, "{" + self.get_xml_ns() + "}" + key)
                sub_element.text = value
        return xml_node

    def send(self):
        self.build_xml_data()
        self.build_query()

        method = self.agent.call_method
        if method == self.CALL_METHOD_AUTO:
            response = self.check_connection()
        elif method == self.CALL_METHOD_CURL:
            response = self.make_curl_call()
        # elif method == self.CALL_METHOD_LEGACY:
        #     response = self.make_legacy_call()
        else:
            raise SzamlaAgentException(SzamlaAgentException.CALL_TYPE_NOT_EXISTS + ": " + method)

        return response

    def build_query(self):
        letters = list("0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
        random.shuffle(letters)
        self.delim = "".join(letters[0: 16])
        query_data = f'--{self.delim}{SzamlaAgentRequest.CRLF}'
        query_data += f'Content-Disposition: form-data; name="{self.filename}"; ' \
                      f'filename="{self.filename}"{SzamlaAgentRequest.CRLF}'
        query_data += f'Content-Type: text/xml{SzamlaAgentRequest.CRLF}{SzamlaAgentRequest.CRLF}'
        query_data += self.xml_data.decode('utf-8') + SzamlaAgentRequest.CRLF
        query_data += f"--{self.delim}--{SzamlaAgentRequest.CRLF}"
        self.post_fields = query_data

    def check_connection(self):
        agent = self.agent
        ch = pycurl.Curl()
        ch.setopt(pycurl.SSL_VERIFYPEER, True)
        ch.setopt(pycurl.SSL_VERIFYHOST, 2)
        ch.setopt(pycurl.CAINFO, agent.get_certification_file)
        ch.setopt(pycurl.NOBODY, True)

        if self.is_basic_auth_request:
            ch.setopt(pycurl.USERPWD, self.get_basic_auth_user_pwd)

        ch.perform()

        code = ch.getinfo(pycurl.HTTP_CODE)
        ch.close()

        if code == SzamlaAgentRequest.HTTP_OK:
            agent.call_method(SzamlaAgentRequest.CALL_METHOD_CURL)
            agent.write_log("Connection type is set to 'CURL'", logging.DEBUG)
            return self.make_curl_call()
        else:
            agent.call_method(SzamlaAgentRequest.CALL_METHOD_LEGACY)
            agent.write_log("Connection type is set to 'LEGACY'", logging.WARN)
            return self.make_curl_call()

    def make_curl_call(self):
        try:
            agent = self.agent
            ch = pycurl.Curl()
            ch.setopt(pycurl.URL, agent.api_url)
            ch.setopt(pycurl.SSL_VERIFYPEER, 1)
            ch.setopt(pycurl.SSL_VERIFYHOST, 2)
            ch.setopt(pycurl.CAINFO, agent.get_certification_file())
            ch.setopt(pycurl.POST, 1)
            ch.setopt(pycurl.HEADER, 1)
            ch.setopt(pycurl.HEADERFUNCTION, self.get_headers_from_response)
            ch.setopt(pycurl.VERBOSE, 1)

            if self.is_basic_auth_request():
                ch.setopt(pycurl.USERPWD, self.get_basic_auth_user_pwd())

            file_upload = [(self.filename, (
                                pycurl.FORM_FILE, self.xml_file_path,
                                pycurl.FORM_FILENAME, self.filename,
                                pycurl.FORM_CONTENTTYPE, 'text/xml'
            ))]

            post_fields = {}

            http_headers = [
                f'charset: {AgentConstant.CHARSET}',
                f'API: {AgentConstant.API_VERSION}'
            ]

            custom_http_headers = agent.custom_http_headers
            if custom_http_headers:
                for key in custom_http_headers:
                    http_headers[key] = f'{key}: {custom_http_headers[key]}'

            ch.setopt(pycurl.HTTPHEADER, http_headers)

            if self.is_attachments():
                attachments = self.entity.attachments
                if attachments:
                    for idx, item in attachments:
                        if os.path.exists(item):
                            is_attachable = True
                            for field in post_fields:
                                if post_fields[field] == item[field]:
                                    is_attachable = False
                                    agent.write_log(f'{idx} has already attached: {item[field]}', logging.DEBUG)

                            if is_attachable:
                                attachment = (self.xml_file_path, open(self.xml_file_path), 'rb', 'text/xml')
                                post_fields[f'attachfile{idx}'] = attachment
                                agent.write_log(f'{idx} document is attached: {item}', logging.DEBUG)

            ch.setopt(pycurl.HTTPPOST, file_upload)
            if len(post_fields) > 0:
                ch.setopt(pycurl.POSTFIELDS, urlencode(post_fields))
            ch.setopt(pycurl.TIMEOUT, SzamlaAgentRequest.REQUEST_TIMEOUT)

            if agent.cookie_file_name:
                cookie_file = self.get_cookie_file_path()
                if os.path.exists(cookie_file) and os.path.getsize(cookie_file) > 0 \
                        and self.file_get_contents(cookie_file, b'curl'):
                    with open(cookie_file, 'a') as file:
                        file.write('')
                        agent.write_log("Cookie has changed", logging.DEBUG)

                ch.setopt(pycurl.COOKIEJAR, cookie_file)
                if os.path.exists(cookie_file) and os.path.getsize(cookie_file) > 0:
                    ch.setopt(pycurl.COOKIEFILE, cookie_file)

            agent.write_log(f"CURL data send is starting: {post_fields}", logging.DEBUG)
            buffer = BytesIO()
            ch.setopt(pycurl.WRITEFUNCTION, buffer.write)
            ch.perform()

            error = ch.errstr()

            headers = self.response_headers
            header_size = ch.getinfo(pycurl.HEADER_SIZE)
            buffer.seek(header_size)
            response = {
                'headers': headers,
                'body': buffer.read()
            }

            buffer.close()
            if error:
                raise SzamlaAgentException(error)
            else:
                keys = ''.join(headers)
                if (response['headers']['content-type']
                        and response['headers']['content-type'] == 'application/pdf') \
                        or not re.search('/(szlahu_)/', keys):
                    message = response['headers']
                else:
                    message = response
                response['headers']['schema-type'] = self.get_xml_schema_type()
                agent.write_log(f'CURL data is successfully ended {message}', logging.DEBUG)

            ch.close()
            return response
        except Exception as ex:
            raise ex

    # def make_legacy_call(self):
    #     try:
    #         agent = self.agent
    #         if self.is_attachments():
    #             raise SzamlaAgentException(SzamlaAgentException.SENDING_ATTACHMENT_NOT_ALLOWED)
    #
    #         cookie_text = ""
    #         cookies = []
    #         stored_cookies = []
    #
    #         cookie_file = self.get_cookie_file_path()
    #         if cookie_file and os.path.exists(cookie_file) and os.path.getsize(cookie_file) > 0 and not self.file_get_contents(cookie_file, 'curl'):
    #             with open(cookie_file, 'r') as f:
    #                 stored_cookies = unserialize(f.read())
    #             cookie_text = f"\r\nCookie: JSESSIONID={stored_cookies['JSESSIONID']}"
    #
    #         http_headers = "Content-Type: multipart/form-data; boundary="
    #
    #     except Exception as ex:
    #         raise ex

    def get_headers_from_response(self, header_line):
        header_line = header_line.decode('iso-8859-1')
        if ':' not in header_line:
            return

        name, value = header_line.split(':', 1)
        name = name.strip()
        value = value.strip()
        name = name.lower()
        value = value.lower()

        self.response_headers[name] = value

    def get_cookie_file_path(self):
        file_name = self.agent.cookie_file_name
        if not file_name:
            file_name = AgentConstant.COOKIE_FILENAME
        return os.path.join(SzamlaAgentUtil.get_base_path(), file_name)

    def file_get_contents(self, file_name, text):
        with open(file_name, 'rb', 0) as f:
            with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as s:
                if s.find(text) != -1:
                    return True
        return False

    def set_xml_file_data(self, type):
        file_name = ''
        xml_name = ''
        xsd_dir = ''
        if type == 'generateProforma' \
                or type == 'generateInvoice' \
                or type == 'generatePrePaymentInvoice' \
                or type == 'generateFinalInvoice' \
                or type == 'generateCorrectiveInvoice' \
                or type == 'generateDeliveryNote':
            file_name = 'action-xmlagentxmlfile'
            xml_name = XmlSchema.XML_SCHEMA_CREATE_INVOICE
            xsd_dir = 'agent'
        elif type == 'generateReverseInvoice':
            file_name = 'action-szamla_agent_st'
            xml_name = XmlSchema.XML_SCHEMA_CREATE_REVERSE_INVOICE
            xsd_dir = 'agentst'
        elif type == 'payInvoice':
            file_name = 'action-szamla_agent_kifiz'
            xml_name = XmlSchema.XML_SCHEMA_PAY_INVOICE
            xsd_dir = 'agentkifiz'
        elif type == 'requestInvoiceData':
            file_name = 'action-szamla_agent_xml'
            xml_name = XmlSchema.XML_SCHEMA_REQUEST_INVOICE_XML
            xsd_dir = 'agentxml'
        elif type == 'requestInvoicePDF':
            file_name = 'action-szamla_agent_pdf'
            xml_name = XmlSchema.XML_SCHEMA_REQUEST_INVOICE_PDF
            xsd_dir = 'agentpdf'
        elif type == 'generateReceipt':
            file_name = 'action-szamla_agent_nyugta_storno'
            xml_name = XmlSchema.XML_SCHEMA_CREATE_RECEIPT
            xsd_dir = 'nyugtacreate'
        elif type == 'generateReverseReceipt':
            file_name = 'action-szamla_agent_nyugta_storno'
            xml_name = XmlSchema.XML_SCHEMA_CREATE_REVERSE_RECEIPT
            xsd_dir = 'nyugtast'
        elif type == 'sendReceipt':
            file_name = 'action-szamla_agent_nyugta_send'
            xml_name = XmlSchema.XML_SCHEMA_SEND_RECEIPT
            xsd_dir = 'nyugtasend'
        elif type == 'requestReceiptData' \
                or type == 'requestReceiptPDF':
            file_name = 'action-szamla_agent_nyugta_get'
            xml_name = XmlSchema.XML_SCHEMA_GET_RECEIPT
            xsd_dir = 'nyugtaget'
        elif type == 'getTaxPayer':
            file_name = 'action-szamla_agent_taxpayer'
            xml_name = XmlSchema.XML_SCHEMA_TAXPAYER
            xsd_dir = 'taxpayer'
        elif type == 'deleteProforma':
            file_name = 'action-szamla_agent_dijbekero_torlese'
            xml_name = XmlSchema.XML_SCHEMA_DELETE_PROFORMA
            xsd_dir = 'dijbekerodel'
        else:
            raise SzamlaAgentException(SzamlaAgentException.REQUEST_TYPE_NOT_EXISTS + f": {type}")

        self.filename = file_name
        self.xml_name = xml_name
        self.xsd_dir = xsd_dir

    def create_xml_file(self, xml):
        file_name = SzamlaAgentUtil.get_xml_file_name('request', self.xml_name, self.entity)
        xml.write(file_name,
                  xml_declaration=True,
                  encoding="utf-8",
                  method='xml')

        self.xml_file_path = SzamlaAgentUtil.get_real_path(file_name)
        self.agent.write_log(f"XML save is succeeded: {self.xml_file_path}", logging.DEBUG)

    def get_xml_schema_type(self):
        if self.xml_name == XmlSchema.XML_SCHEMA_CREATE_INVOICE \
                or self.xml_name == XmlSchema.XML_SCHEMA_CREATE_REVERSE_INVOICE \
                or self.xml_name == XmlSchema.XML_SCHEMA_PAY_INVOICE \
                or self.xml_name == XmlSchema.XML_SCHEMA_REQUEST_INVOICE_XML \
                or self.xml_name == XmlSchema.XML_SCHEMA_REQUEST_INVOICE_PDF:
            return DocumentConstant.DOCUMENT_TYPE_INVOICE
        # if self.XML_SCHEMA_DELETE_PROFORMA:
        #     return Document.DOCUMENT_TYPE_INVOICE
        raise SzamlaAgentException(SzamlaAgentException.XML_SCHEMA_TYPE_NOT_EXISTS + f": {self.xml_name}")

    def is_attachments(self):
        entity = self.entity
        from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.document.invoice.invoice import Invoice
        if isinstance(entity, Invoice):
            return len(entity.attachments) > 0
        return False

    def is_basic_auth_request(self):
        agent = self.agent
        return agent.environment and agent.get_environment_auth_type() == self.REQUEST_AUTHORIZATION_BASIC_AUTH

    def get_basic_auth_user_pwd(self):
        return self.agent.get_environment_auth_user() + ":" + self.agent.get_environment_auth_password()

    def get_schema_location(self):
        return f"{SzamlaAgentRequest.XML_BASE_URL}szamla/{self.xml_name} " \
               f"{SzamlaAgentRequest.XML_BASE_URL}szamla/docs/xsds/{self.xsd_dir}/{self.xml_name}.xsd"

    def get_xml_ns(self):
        return f"{SzamlaAgentRequest.XML_BASE_URL}{self.xml_name}"
