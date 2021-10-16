import logging
import pycurl

from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.exception.szamla_agent_exception import \
    SzamlaAgentException
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.szamla_agent import SzamlaAgent
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.szamla_agent_util import SzamlaAgentUtil


class SzamlaAgentRequest:
    HTTP_OK = 200
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

    # Számlakészítéshez használt XML séma
    # @ see https: // www.szamlazz.hu / szamla / docs / xsds / agent / xmlszamla.xsd
    XML_SCHEMA_CREATE_INVOICE = 'xmlszamla'

    # Számla sztornózásához használt XML séma
    # @ see https: // www.szamlazz.hu / szamla / docs / xsds / agentst / xmlszamlast.xsd
    XML_SCHEMA_CREATE_REVERSE_INVOICE = 'xmlszamlast'

    # Jóváírás rögzítéséhez használt XML séma
    # @ see https: // www.szamlazz.hu / szamla / docs / xsds / agentkifiz / xmlszamlakifiz.xsd
    XML_SCHEMA_PAY_INVOICE = 'xmlszamlakifiz'

    # Számla adatok lekéréséhez használt XML séma
    # @ see https: // www.szamlazz.hu / szamla / docs / xsds / agentxml / xmlszamlaxml.xsd
    XML_SCHEMA_REQUEST_INVOICE_XML = 'xmlszamlaxml'

    # Számla PDF lekéréséhez használt XML séma
    # @ see https: // www.szamlazz.hu / szamla / docs / xsds / agentpdf / xmlszamlapdf.xsd
    XML_SCHEMA_REQUEST_INVOICE_PDF = 'xmlszamlapdf'

    # Nyugta készítéséhez használt XML séma
    # @ see https: // www.szamlazz.hu / szamla / docs / xsds / nyugtacreate / xmlnyugtacreate.xsd
    XML_SCHEMA_CREATE_RECEIPT = 'xmlnyugtacreate'

    # Nyugta sztornóhoz használt XML séma
    # @ see https: // www.szamlazz.hu / szamla / docs / xsds / nyugtast / xmlnyugtast.xsd
    XML_SCHEMA_CREATE_REVERSE_RECEIPT = 'xmlnyugtast'

    # Nyugta kiküldéséhez használt XML séma
    # @ see https: // www.szamlazz.hu / szamla / docs / xsds / nyugtasend / xmlnyugtasend.xsd
    XML_SCHEMA_SEND_RECEIPT = 'xmlnyugtasend'

    # Nyugta megjelenítéséhez használt XML séma
    # @ see https: // www.szamlazz.hu / szamla / docs / xsds / nyugtaget / xmlnyugtaget.xsd
    XML_SCHEMA_GET_RECEIPT = 'xmlnyugtaget'

    # Adózó adatainak lekérdezéséhez használt XML séma
    # @ see https: // www.szamlazz.hu / szamla / docs / xsds / taxpayer / xmltaxpayer.xsd
    XML_SCHEMA_TAXPAYER = 'xmltaxpayer'

    # Díjbekérő törléséhez használt XML séma
    # @ see https: // www.szamlazz.hu / szamla / docs / xsds / dijbekerodel / xmlszamladbkdel.xsd
    XML_SCHEMA_DELETE_PROFORMA = 'xmlszamladbkdel'

    # Kérés engedélyezési módok
    REQUEST_AUTHORIZATION_BASIC_AUTH = 1

    @property
    def agent(self):
        return self.__agent

    @agent.setter
    def agent(self, value):
        if not isinstance(value, SzamlaAgent):
            raise TypeError('agent must be an SzamlaAgent')
        self.__agent = value

    def __init__(self, agent, request_type, entity):
        self.agent = agent
        self.type = request_type
        self.entity = entity
        self.cData = True
        self.fileName = ''
        self.xmlName = ''
        self.xsdDir = ''
        self.xmlData = ''
        self.xmlFilePath = ''

    def build_xml_data(self):
        self.set_xml_file_data(self.type)
        agent = self.agent
        agent.write_log("Collecting XML data is starting", logging.DEBUG)
        xml_data = self.entity.build_xml_data(self)

        xml = self.array_to_xml(xml_data)
        try:
            result = SzamlaAgentUtil.check_valid_xml(xml.save())
            if not result:
                raise SzamlaAgentException(SzamlaAgentException.XML_NOT_VALID + f"in line {result[0].line}: {result[o].message}")
            format_xml = SzamlaAgentUtil.format_xml(xml)
            self.xmlData = format_xml
            agent.write_log("Collection XML data has done.", logging.DEBUG)
            self.create_xml_file(format_xml)
        except Exception as ex:
            raise SzamlaAgentException(SzamlaAgentException.XML_DATA_BUILD_FAILED + format(ex))

    def send(self):
        self.build_xml_data()
        self.build_query()

        method = self.agent.callMethod
        if method == self.CALL_METHOD_AUTO:
            response = self.check_connection()
        elif method == self.CALL_METHOD_CURL:
            response = self.make_curl_call()
        elif method == self.CALL_METHOD_LEGACY:
            response = self.make_legacy_call()
        else:
            raise SzamlaAgentException(SzamlaAgentException.CALL_TYPE_NOT_EXISTS + ": " + method)

        return response

    def check_connection(self):
        agent = self.agent
        ch = pycurl.Curl()
        ch.setopt(pycurl.SSL_VERIFYPEER, True)
        ch.setopt(pycurl.SSL_VERIFYHOST, 2)
        ch.setopt(pycurl.CAINFO, agent.certificationFile())
        ch.setopt(pycurl.NOBODY, True)

        if self.is_basic_auth_request():
            ch.setopt(pycurl.USERPWD, self.basic_auth_user_pwd())

        ch.perform()

        code = ch.getinfo(pycurl.HTTP_CODE)
        ch.close()

        if code == SzamlaAgentRequest.HTTP_OK:
            agent.callMethod(SzamlaAgentRequest.CALL_METHOD_CURL)
            agent.write_log("Connection type is set to 'CURL'", logging.DEBUG)
            return self.make_curl_call()
        else:
            agent.callMethod(SzamlaAgentRequest.CALL_METHOD_LEGACY)
            agent.write_log("Connection type is set to 'LEGACY'", logging.WARN)
            return self.make_curl_call()

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
            xml_name = SzamlaAgentRequest.XML_SCHEMA_CREATE_INVOICE
            xsd_dir = 'agent'
        elif type == 'generateReverseInvoice':
            file_name = 'action-szamla_agent_st'
            xml_name = SzamlaAgentRequest.XML_SCHEMA_CREATE_REVERSE_INVOICE
            xsd_dir = 'agentst'
        elif type == 'payInvoice':
            file_name = 'action-szamla_agent_kifiz'
            xml_name = SzamlaAgentRequest.XML_SCHEMA_PAY_INVOICE
            xsd_dir = 'agentkifiz'
        elif type == 'requestInvoiceData':
            file_name = 'action-szamla_agent_xml'
            xml_name = SzamlaAgentRequest.XML_SCHEMA_REQUEST_INVOICE_XML
            xsd_dir = 'agentxml'
        elif type == 'requestInvoicePDF':
            file_name = 'action-szamla_agent_pdf'
            xml_name = SzamlaAgentRequest.XML_SCHEMA_REQUEST_INVOICE_PDF
            xsd_dir = 'agentpdf'
        elif type == 'generateReceipt':
            file_name = 'action-szamla_agent_nyugta_storno'
            xml_name = SzamlaAgentRequest.XML_SCHEMA_CREATE_RECEIPT
            xsd_dir = 'nyugtacreate'
        elif type == 'generateReverseReceipt':
            file_name = 'action-szamla_agent_nyugta_storno'
            xml_name = SzamlaAgentRequest.XML_SCHEMA_CREATE_REVERSE_RECEIPT
            xsd_dir = 'nyugtast'
        elif type == 'sendReceipt':
            file_name = 'action-szamla_agent_nyugta_send'
            xml_name = SzamlaAgentRequest.XML_SCHEMA_SEND_RECEIPT
            xsd_dir = 'nyugtasend'
        elif type == 'requestReceiptData' \
                or type == 'requestReceiptPDF':
            file_name = 'action-szamla_agent_nyugta_get'
            xml_name = SzamlaAgentRequest.XML_SCHEMA_GET_RECEIPT
            xsd_dir = 'nyugtaget'
        elif type == 'getTaxPayer':
            file_name = 'action-szamla_agent_taxpayer'
            xml_name = SzamlaAgentRequest.XML_SCHEMA_TAXPAYER
            xsd_dir = 'taxpayer'
        elif type == 'deleteProforma':
            file_name = 'action-szamla_agent_dijbekero_torlese'
            xml_name = SzamlaAgentRequest.XML_SCHEMA_DELETE_PROFORMA
            xsd_dir = 'dijbekerodel'
        else:
            raise SzamlaAgentException(SzamlaAgentException.REQUEST_TYPE_NOT_EXISTS + f": {type}")

        self.fileName = file_name
        self.xmlName = xml_name
        self.xsdDir = xsd_dir

    def create_xml_file(self, xml):
        file_name = SzamlaAgentUtil.get_xml_file_name('request', self.xmlName, self.entity)
        xml.write(file_name)

        self.xmlFilePath = SzamlaAgentUtil.get_real_path(file_name)
        self.agent.write_log(f"XML save is succeeded: {self.xmlFilePath}", logging.DEBUG)
