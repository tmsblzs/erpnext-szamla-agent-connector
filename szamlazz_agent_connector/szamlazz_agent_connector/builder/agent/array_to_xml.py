import xml.etree.ElementTree as ET
from html import escape


class ArrayToXml:
    @staticmethod
    def convert(xml_data, xml_node, xml_ns):
        for key in xml_data:
            if isinstance(xml_data[key], dict):
                field_key = key
                if key.find("item") != -1:
                    field_key = 'tetel'
                if key.find("note") != -1:
                    field_key = 'kifizetes'
                sub_node = ET.SubElement(xml_node, "{" + xml_ns + "}" + field_key)
                ArrayToXml.convert(xml_data[key], sub_node, xml_ns)
            else:
                if isinstance(xml_data[key], bool):
                    value = 'true' if xml_data[key] else 'false'
                if isinstance(xml_data[key], (int, float)):
                    value = str(xml_data[key]).lower()
                else:
                    value = escape(xml_data[key])

                sub_element = ET.SubElement(xml_node, "{" + xml_ns + "}" + key)
                sub_element.text = value
        return xml_node
