import hashlib
import os
import mmap

from szamlazz_agent_connector.szamlazz_agent_connector.model.constant.agent_constant import AgentConstant
from szamlazz_agent_connector.szamlazz_agent_connector.model.szamla_agent_util import SzamlaAgentUtil


class SzamlaAgentCookie:
    def __init__(self, username, api_key):
        self._username = username
        self._api_key = api_key
        self._filename = self._build_cookie_filename()

    @property
    def filename(self):
        return self._filename

    def _build_cookie_filename(self):
        filename = 'cookie/cookie'
        username = self._username
        apikey = self._api_key

        if username:
            filename += "_" + hashlib.sha1(username.encode('utf-8')).hexdigest()
        elif apikey:
            filename += "_" + hashlib.sha1(apikey.encode('utf-8')).hexdigest()

        return filename + '.txt'

    def get_file_path(self):
        if not self.filename:
            self._filename = AgentConstant.COOKIE_FILENAME
        return os.path.join(SzamlaAgentUtil.get_base_path(), self.filename)

    def get_contents(self,  text):
        with open(self.filename, 'rb', 0) as f:
            with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as s:
                if s.find(text) != -1:
                    return True
        return False
