from szamlazz_agent_connector.szamlazz_agent_connector.model.szamla_agent_util import SzamlaAgentUtil
from szamlazz_agent_connector.szamlazz_agent_connector.validator.base_validator import BaseValidator


class SellerValidator(BaseValidator):
    def _check_field(self, field, value):
        if hasattr(self, field):
            if field == 'bank' \
                    or field == 'bankAccount' \
                    or field == 'emailReplyTo' \
                    or field == 'emailSubject' \
                    or field == 'emailContent' \
                    or field == 'signatoryName':
                SzamlaAgentUtil.check_str_field(field, value, False, type(self).__name__)
        return value
