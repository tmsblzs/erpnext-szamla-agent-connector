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

    agent = ''

    # A Számla Agent kérés típusa
    # @ see SzamlaAgentRequest::getActionName()
    # @ var string
    type = ''

    # Azaz entitás, amelynek adatait XML formátumban továbbítani fogjuk
    # (számla, díjbekérő, szállítólevél, adózó, stb.)
    # @ var object
    entity = ''

    # Az Agent kéréshez összeállított XML adatok
    # @ var string
    xmlData = ''

    # XML gyökérelem neve
    # @ var string
    xmlName = ''

    # XML fájl elérési útvonala
    # @ var string
    xmlFilePath = ''

    # XSD könyvtárának neve
    # @ var string
    xsdDir = ''

    # Számla Agent kérés XML fájlneve
    # @ var string
    fileName = ''

    # Egyedi elválasztó azonosító az XML kéréshez
    # @ var string
    delim = ''

    # Az Agent kérésnél továbbított POST adatok
    # @ var string
    postFields = ''

    # Az Agent kéréshez tartozó adatok CDATA - ként lesznek átadva
    # @ var boolean
    cData = True

    def __init__(self, agent, request_type, entity):
        self.agent = agent
        self.type = request_type
        self.entity = entity
        self.cData = True

    def send(self):
        pass

