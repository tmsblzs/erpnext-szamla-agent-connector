import datetime
import locale
import logging
import os
import re
from pathlib import Path
from xml.dom.minidom import minidom
from xml.etree import ElementTree
from xml.etree.ElementTree import ParseError

from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.exception.szamla_agent_exception import \
    SzamlaAgentException
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.szamla_agent import SzamlaAgent


class SzamlaAgentUtil:
    DEFAULT_ADDED_DAYS = 8

    DEFAULT_BASE_PATH = f".{os.pathsep}..{os.pathsep}..{os.pathsep}"

    DATE_FORMAT_DATE = "%Y-%m-d"

    DATE_FORMAT_DATETIME = "%Y-%m-d %H:%M:%S"

    DATE_FORMAT_TIMESTAMP = 'timestamp'

    basePath = DEFAULT_BASE_PATH


    @staticmethod
    def add_days_to_date(count, date=None):
        new_date = datetime.datetime.today()

        if date:
            new_date = datetime.datetime.strptime(date, "%Y-%m-d")
        new_date = new_date + datetime.timedelta(days=count)
        return SzamlaAgentUtil.get_date_str(new_date)

    @staticmethod
    def get_date_str(date: datetime, date_format=DATE_FORMAT_DATE):
        if date_format == SzamlaAgentUtil.DATE_FORMAT_TIMESTAMP:
            result = date.timestamp()
        else:
            result = date.strftime(date_format)
        return result

    @staticmethod
    def get_today_str():
        return datetime.datetime.today().strftime(SzamlaAgentUtil.DATE_FORMAT_DATE)

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
    def format_xml(xml):
        return ElementTree.parse(xml)

    @staticmethod
    def check_valid_xml(xml):
        try:
            ElementTree.fromstring(xml)
            return True
        except ParseError:
            return False

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

    @staticmethod
    def number_format(num, places=0):
        return locale.format_string("%.*f", (places, num), True)

    @staticmethod
    def float_format(value):
        if isinstance(value, int):
            value = float(value)

        if isinstance(value, float):
            decimals = len(re.sub(r'/[\d]+[\.]?/', '', value))
            if decimals == 0:
                value = SzamlaAgentUtil.number_format(value, 1)
        else:
            logging.warning(f"Not valid type!, Instead of float got {type(value)} for this value: {value}")
        return value

    @staticmethod
    def check_str_field(field, value, required, class_name):
        error_message = ""
        if value and not isinstance(value, str):
            error_message = f"The {field} attribute value is not a string!"
        elif required and not value:
            error_message = SzamlaAgentUtil.get_required_field_error_message(field)

        if error_message:
            raise SzamlaAgentException(SzamlaAgentException.FIELDS_CHECK_ERROR +
                                       f": {error_message} ({class_name})")

    @staticmethod
    def check_int_field(field, value, required, class_name):
        error_message = ""
        if value and not isinstance(value, int):
            error_message = f"The {field} attribute value is not an integer!"
        elif required and not value:
            error_message = SzamlaAgentUtil.get_required_field_error_message(field)

        if error_message:
            raise SzamlaAgentException(SzamlaAgentException.FIELDS_CHECK_ERROR +
                                       f": {error_message} ({class_name})")

    @staticmethod
    def check_float_field(field, value, required, class_name):
        error_message = ""
        if value and not isinstance(value, float):
            error_message = f"The {field} attribute value is not a float!"
        elif required and not value:
            error_message = SzamlaAgentUtil.get_required_field_error_message(field)

        if error_message:
            raise SzamlaAgentException(SzamlaAgentException.FIELDS_CHECK_ERROR +
                                       f": {error_message} ({class_name})")

    @staticmethod
    def check_date_field(field, value, required, class_name):
        error_message = ""
        if value and not SzamlaAgentUtil.is_valid_date(value):
            if required:
                error_message = f"The {field} is required, but contains a not valid date!"
            else:
                error_message = f"The {field} is not a valid date!"
        if error_message:
            raise SzamlaAgentException(SzamlaAgentException.FIELDS_CHECK_ERROR + f": {error_message} ({class_name})")

    @staticmethod
    def check_bool_field(field, value, required, class_name):
        error_message = ""
        if value and not isinstance(value, bool):
            if required:
                error_message = f"The {field} is required, but not boolean!"
            else:
                error_message = f"The {field} is not a boolean!"

        if error_message:
            raise SzamlaAgentException(SzamlaAgentException.FIELDS_CHECK_ERROR + f": {error_message} ({class_name})")

    @staticmethod
    def get_required_field_error_message(field):
        return f"The {field} is required, but has no value!"

    @staticmethod
    def is_valid_date(date):
        date_format = "%Y-%m-d"
        try:
            datetime.datetime.strptime(date, date_format)
            return True
        except ValueError:
            return False