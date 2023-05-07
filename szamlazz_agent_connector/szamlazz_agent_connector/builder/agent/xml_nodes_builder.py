import xml.etree.ElementTree as ET

from szamlazz_agent_connector.szamlazz_agent_connector.builder.agent.array_to_xml import ArrayToXml


class XmlNodesBuilder:
    XML_BASE_URL = 'http://www.szamlazz.hu/'
    XMLNS_XSI_NAME = 'xmlns:xsi'
    XMLNS_XSI_URL = 'http://www.w3.org/2001/XMLSchema-instance'
    XSI_SCHEMA_LOCATION_NAME = 'xsi:schemaLocation'

    @staticmethod
    def build(entity, xml_data):
        xml_ns = _get_xml_ns(entity)
        ET.register_namespace('', xml_ns)
        xml_node = ET.Element("{" + xml_ns + "}" + entity.xml_name,
                              **{XmlNodesBuilder.XMLNS_XSI_NAME: XmlNodesBuilder.XMLNS_XSI_URL},
                              **{XmlNodesBuilder.XSI_SCHEMA_LOCATION_NAME: _get_schema_location(entity)})
        ArrayToXml.convert(xml_data, xml_node, xml_ns)
        return xml_node


def _get_schema_location(entity):
    return f"{XmlNodesBuilder.XML_BASE_URL}szamla/{entity.xml_name} " \
           f"{XmlNodesBuilder.XML_BASE_URL}szamla/docs/xsds/{entity.xsd_dir}/{entity.xml_name}.xsd"


def _get_xml_ns(entity):
    return f"{XmlNodesBuilder.XML_BASE_URL}{entity.xml_name}"
