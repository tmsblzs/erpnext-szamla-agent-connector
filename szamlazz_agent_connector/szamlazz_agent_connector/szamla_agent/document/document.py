from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.currency import Currency
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.language import Language


class Document:
    @staticmethod
    def get_default_currency():
        return Currency.get_default()

    @staticmethod
    def get_default_language():
        return Language.get_default()
