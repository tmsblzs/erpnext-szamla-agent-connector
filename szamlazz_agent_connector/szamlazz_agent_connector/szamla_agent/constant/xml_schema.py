class XmlSchema:
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
