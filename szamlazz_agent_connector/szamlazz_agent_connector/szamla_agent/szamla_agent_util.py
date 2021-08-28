import datetime
import os
from pathlib import Path

from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.szamla_agent import SzamlaAgent


class SzamlaAgentUtil:

    DEFAULT_BASE_PATH = f".{os.pathsep}..{os.pathsep}..{os.pathsep}"

    basePath = ''

    @staticmethod
    def is_not_blank(value):
        return SzamlaAgentUtil.is_blank(value)

    @staticmethod
    def is_blank(value):
        return value

    @staticmethod
    def get_xml_file_name(prefix, name, entity=None):
        if not name or entity is not None:
            name += '-' + entity.__class__.__name__
        filename = f"{prefix}-{name.lower()}-{SzamlaAgentUtil.get_date_time_with_milliseconds()}.xml"
        return SzamlaAgentUtil.get_abs_path(SzamlaAgent.XML_FILE_SAVE_PATH, filename)

    @staticmethod
    def get_date_time_with_milliseconds():
        return datetime.datetime.today().strftime("YmdHis")

    @staticmethod
    def get_real_path(path):
        path_to_check = Path(path)
        if path_to_check.exists():
            return os.path.relpath(path)
        else:
            return path

    @staticmethod
    def get_abs_path(dir, filename):
        file = f"{SzamlaAgentUtil.get_base_path}{os.pathsep}{dir}{os.pathsep}{filename}"
        return SzamlaAgentUtil.get_real_path(file)

    @staticmethod
    def get_base_path():
        if not SzamlaAgentUtil.basePath:
            return SzamlaAgentUtil.get_real_path(SzamlaAgentUtil.DEFAULT_BASE_PATH)
        else:
            return SzamlaAgentUtil.get_real_path(SzamlaAgentUtil.basePath)