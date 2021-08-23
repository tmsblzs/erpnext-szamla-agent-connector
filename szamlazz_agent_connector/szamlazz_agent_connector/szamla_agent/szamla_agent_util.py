class SzamlaAgentUtil:
    @staticmethod
    def is_not_blank(value):
        return SzamlaAgentUtil.is_blank(value)

    @staticmethod
    def is_blank(value):
        return value
