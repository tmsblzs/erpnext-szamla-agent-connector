import logging
import xml.etree.ElementTree as ET
from io import BytesIO

from szamlazz_agent_connector.szamlazz_agent_connector.builder.agent.xml_nodes_builder import XmlNodesBuilder
from szamlazz_agent_connector.szamlazz_agent_connector.builder.build_xml_data import build_xml_data
from szamlazz_agent_connector.szamlazz_agent_connector.model.exception.szamla_agent_exception import \
    SzamlaAgentException
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.szamla_agent_request import SzamlaAgentRequest
from szamlazz_agent_connector.szamlazz_agent_connector.model.szamla_agent_util import SzamlaAgentUtil


class RequestXmlBuilder:
    # Számla Agent XML séma alapértelmezett URL
    # (az XML generálásához használjuk, ne változtasd meg)

    LF = "/n"

    @staticmethod
    def build(request: SzamlaAgentRequest):
        agent = request.agent
        entity = request.entity
        agent.write_log("Collecting XML data is starting", logging.DEBUG)
        xml_data = build_xml_data(entity, request)

        xml_node = XmlNodesBuilder.build(entity, xml_data)
        try:
            xml_text = get_xml_text(xml_node)
        except Exception as ex:
            raise SzamlaAgentException(f"{SzamlaAgentException.XML_DATA_BUILD_FAILED} {format(ex)}")
        else:
            result = SzamlaAgentUtil.check_valid_xml(xml_text)
            if not result:
                raise SzamlaAgentException(
                    SzamlaAgentException.XML_NOT_VALID + f"in line {result[0].line}: {result[0].message}")
            xml_str = xml_text.replace(bytearray(RequestXmlBuilder.LF, 'utf-8'), bytearray('', 'utf-8'))

            agent.write_log("Collection XML data has done.", logging.DEBUG)
            return xml_str


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





