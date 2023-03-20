import logging
import xml.etree.ElementTree as ET
from html import escape
from io import BytesIO

from szamlazz_agent_connector.szamlazz_agent_connector.builder.build_xml_data import build_xml_data
from szamlazz_agent_connector.szamlazz_agent_connector.builder.query.query_builder import QueryBuilder
from szamlazz_agent_connector.szamlazz_agent_connector.model.exception.szamla_agent_exception import \
    SzamlaAgentException
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.szamla_agent_request import SzamlaAgentRequest
from szamlazz_agent_connector.szamlazz_agent_connector.model.szamla_agent_util import SzamlaAgentUtil


class RequestXmlBuilder:
    # Számla Agent XML séma alapértelmezett URL
    # (az XML generálásához használjuk, ne változtasd meg)
    XML_BASE_URL = 'http://www.szamlazz.hu/'
    XMLNS_XSI_NAME = 'xmlns:xsi'
    XMLNS_XSI_URL = 'http://www.w3.org/2001/XMLSchema-instance'
    XSI_SCHEMA_LOCATION_NAME = 'xsi:schemaLocation'

    def __init__(self):
        self._c_data = True

    def build_xml(self, request: SzamlaAgentRequest):
        agent = request.agent
        entity = request.entity
        agent.write_log("Collecting XML data is starting", logging.DEBUG)
        xml_data = build_xml_data(entity, request)

        xml_node = self.build_xml_nodes(entity, xml_data)
        try:
            xml_text = get_xml_text(xml_node)
        except Exception as ex:
            raise SzamlaAgentException(f"{SzamlaAgentException.XML_DATA_BUILD_FAILED} {format(ex)}")
        else:
            result = SzamlaAgentUtil.check_valid_xml(xml_text)
            if not result:
                raise SzamlaAgentException(
                    SzamlaAgentException.XML_NOT_VALID + f"in line {result[0].line}: {result[0].message}")
            xml_str = xml_text.replace(bytearray(QueryBuilder.LF, 'utf-8'), bytearray('', 'utf-8'))

            agent.write_log("Collection XML data has done.", logging.DEBUG)
            return xml_text

    def build_xml_nodes(self, entity, xml_data):
        xml_ns = get_xml_ns(entity)
        ET.register_namespace('', xml_ns)
        xml_node = ET.Element("{" + xml_ns + "}" + entity.xml_name,
                              **{RequestXmlBuilder.XMLNS_XSI_NAME: RequestXmlBuilder.XMLNS_XSI_URL},
                              **{RequestXmlBuilder.XSI_SCHEMA_LOCATION_NAME: get_schema_location(entity)})
        self.array_to_xml(xml_data, xml_node, xml_ns)
        return xml_node

    def array_to_xml(self, xml_data, xml_node, xml_ns):
        for key in xml_data:
            if isinstance(xml_data[key], dict):
                field_key = key
                if key.find("item") != -1:
                    field_key = 'tetel'
                if key.find("note") != -1:
                    field_key = 'kifizetes'
                sub_node = ET.SubElement(xml_node, "{" + xml_ns + "}" + field_key)
                self.array_to_xml(xml_data[key], sub_node, xml_ns)
            else:
                if isinstance(xml_data[key], bool):
                    value = 'true' if xml_data[key] else 'false'
                if isinstance(xml_data[key], (int, float)):
                    value = str(xml_data[key]).lower()
                else:
                    value = xml_data[key]

                sub_element = ET.SubElement(xml_node, "{" + xml_ns + "}" + key)
                sub_element.text = value
        return xml_node


def get_xml_text(xml_node):
    et = ET.ElementTree(xml_node)
    f = BytesIO()
    et.write(f,
             encoding='utf-8',
             xml_declaration=False,
             method='xml')
    xml_text = f.getvalue()
    f.close()
    return xml_text


def get_schema_location(entity):
    return f"{RequestXmlBuilder.XML_BASE_URL}szamla/{entity.xml_name} " \
           f"{RequestXmlBuilder.XML_BASE_URL}szamla/docs/xsds/{entity.xsd_dir}/{entity.xml_name}.xsd"


def get_xml_ns(entity):
    return f"{RequestXmlBuilder.XML_BASE_URL}{entity.xml_name}"



