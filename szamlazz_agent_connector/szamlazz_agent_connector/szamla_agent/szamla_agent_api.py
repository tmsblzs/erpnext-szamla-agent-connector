import logging

from szamlazz_agent_connector.szamlazz_agent_connector.model.constant.response_constant import ResponseConstant
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.szamla_agent import \
    SzamlaAgent


class SzamlaAgentApi(SzamlaAgent):
    @staticmethod
    def create(api_key,
               download_pdf=True,
               log_level=logging.DEBUG,
               response_type=ResponseConstant.RESULT_AS_TEXT,
               aggregator=""):
        index = SzamlaAgent.get_hash(api_key)

        agent = None
        if index in SzamlaAgent.agents:
            agent = SzamlaAgent.agents[index]

        if agent is None:
            agent = SzamlaAgent(None, None, api_key, download_pdf, log_level, response_type, aggregator)
            SzamlaAgent.agents[index] = agent

        return agent
