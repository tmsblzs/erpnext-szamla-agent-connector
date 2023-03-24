import logging
import os
import re
from html import escape
from io import BytesIO

import pycurl

from szamlazz_agent_connector.szamlazz_agent_connector.model.constant.agent_constant import AgentConstant
from szamlazz_agent_connector.szamlazz_agent_connector.model.exception.szamla_agent_exception import \
    SzamlaAgentException


class CurlService:
    HTTP_OK = 200

    # Számla Agent kérés maximális idő másodpercben
    REQUEST_TIMEOUT = 30
    # Kérés engedélyezési módok
    REQUEST_AUTHORIZATION_BASIC_AUTH = 1

    def __init__(self):
        self._response_headers = {}
        self._curl = pycurl.Curl()

    def make_call(self, agent, entity, query_xml):
        self.setup_call(agent)
        if self.is_basic_auth_request(agent):
            self._curl.setopt(pycurl.USERPWD, self.get_basic_auth_user_pwd(agent))

        self.set_headers(agent)
        self.set_data_for_sending(entity, query_xml)
        post_fields = self.set_attachments(agent, entity, {})
        self.set_cookie(agent)

        agent.write_log(f"CURL data send is starting: {post_fields}", logging.DEBUG)
        error, headers, response = self.call_and_get_response()
        if error:
            agent.write_log(f'CURL data sending failed!', logging.DEBUG)
            raise SzamlaAgentException(error)
        else:
            message = self.get_response_message(headers, response)
            response['headers']['schema-type'] = entity.xml_schema_type
            agent.write_log(f'CURL data is successfully ended {message}', logging.DEBUG)

        self._curl.close()
        return response

    def get_response_message(self, headers, response):
        keys = ''.join(headers)
        if (response['headers']['content-type']
            and response['headers']['content-type'] == 'application/pdf') \
                or not re.search('/(szlahu_)/', keys):
            message = response['headers']
        else:
            message = response
        return message

    def call_and_get_response(self):
        buffer = BytesIO()
        self._curl.setopt(pycurl.WRITEFUNCTION, buffer.write)
        self._curl.perform()
        error = self._curl.errstr()
        headers = self._response_headers
        header_size = self._curl.getinfo(pycurl.HEADER_SIZE)
        buffer.seek(header_size)
        response = {
            'headers': headers,
            'body': buffer.read()
        }
        buffer.close()
        return error, headers, response

    def set_cookie(self, agent):
        if agent.cookie.filename:
            cookie_file = agent.cookie.get_file_path()
            if os.path.exists(cookie_file) and os.path.getsize(cookie_file) > 0 \
                    and agent.cookie.get_contents(b'curl'):
                with open(cookie_file, 'a') as file:
                    file.write('')
                    agent.write_log("Cookie has changed", logging.DEBUG)

            self._curl.setopt(pycurl.COOKIEJAR, cookie_file)
            if os.path.exists(cookie_file) and os.path.getsize(cookie_file) > 0:
                self._curl.setopt(pycurl.COOKIEFILE, cookie_file)

    def set_data_for_sending(self, entity, query_xml):
        file_upload = [(entity.filename, (
            pycurl.FORM_BUFFERPTR, query_xml,
            pycurl.FORM_BUFFER, entity.filename,
            pycurl.FORM_CONTENTTYPE, 'text/xml'
        ))]
        self._curl.setopt(pycurl.HTTPPOST, file_upload)

    def set_attachments(self, agent, entity, post_fields):
        if entity.is_attachments:
            attachments = entity.attachments
            if attachments:
                for idx, item in attachments:
                    if os.path.exists(item):
                        is_attachable = True
                        for field in post_fields:
                            if post_fields[field] == item[field]:
                                is_attachable = False
                                agent.write_log(f'{idx} has already attached: {item[field]}', logging.DEBUG)

                        if is_attachable:
                            attachment = (entity.xml_file_path, open(entity.xml_file_path), 'rb', 'text/xml')
                            post_fields[f'attachfile{idx}'] = attachment
                            agent.write_log(f'{idx} document is attached: {item}', logging.DEBUG)
        if len(post_fields) > 0:
            self._curl.setopt(pycurl.POSTFIELDS, post_fields)
        return post_fields

    def set_headers(self, agent):
        http_headers = [
            f'charset: {AgentConstant.CHARSET}',
            f'API: {AgentConstant.API_VERSION}'
        ]
        custom_http_headers = agent.custom_http_headers
        if custom_http_headers:
            for key in custom_http_headers:
                http_headers[key] = f'{key}: {custom_http_headers[key]}'
        self._curl.setopt(pycurl.HTTPHEADER, http_headers)

    def setup_call(self, agent):
        self._curl.setopt(pycurl.URL, agent.api_url)
        self._curl.setopt(pycurl.SSL_VERIFYPEER, 1)
        self._curl.setopt(pycurl.SSL_VERIFYHOST, 2)
        self._curl.setopt(pycurl.CAINFO, agent.get_certification_file())
        self._curl.setopt(pycurl.POST, 1)
        self._curl.setopt(pycurl.HEADER, 1)
        self._curl.setopt(pycurl.HEADERFUNCTION, self.get_headers_from_response)
        self._curl.setopt(pycurl.VERBOSE, 1)
        self._curl.setopt(pycurl.TIMEOUT, CurlService.REQUEST_TIMEOUT)

    def get_headers_from_response(self, header_line):
        header_line = header_line.decode('iso-8859-1')
        if ':' not in header_line:
            return

        name, value = header_line.split(':', 1)
        name = name.strip()
        value = value.strip()
        name = name.lower()
        value = value.lower()

        self._response_headers[name] = value

    def is_basic_auth_request(self, agent):
        return agent.environment \
               and agent.get_environment_auth_type() == CurlService.REQUEST_AUTHORIZATION_BASIC_AUTH

    def get_basic_auth_user_pwd(self,agent):
        return agent.get_environment_auth_user() + ":" + agent.get_environment_auth_password()
