import inspect

from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.szamla_agent_util import SzamlaAgentUtil


class Item:
    # Áfakulcs: tárgyi adómentes
    VAT_TAM = 'TAM'

    # Áfakulcs: alanyi adómentes
    VAT_AAM = 'AAM'

    # Áfakulcs: EU - n belül
    VAT_EU = 'EU'

    # Áfakulcs: EU - n kívül
    VAT_EUK = 'EUK'

    # Áfakulcs: mentes az adó alól
    VAT_MAA = 'MAA'

    # Áfakulcs: fordított áfa
    VAT_F_AFA = 'F.AFA'

    # Áfakulcs: különbözeti áfa
    VAT_K_AFA = 'K.AFA'

    # Áfakulcs: áfakörön kívüli
    VAT_AKK = 'ÁKK'

    # Áfakulcs: áfakörön kívüli
    VAT_TAHK = 'TAHK'

    # Áfakulcs: áfakörön kívüli
    VAT_TEHK = 'TEHK'

    # Áfakulcs: EU - n belüli termék értékesítés
    VAT_EUT = 'EUT'

    # Áfakulcs: EU - n kívüli termék értékesítés
    VAT_EUKT = 'EUKT'

    # Áfakulcs: EU - n belüli
    VAT_KBAET = 'KBAET'

    # Áfakulcs: EU - n belüli
    VAT_KBAUK = 'KBAUK'

    # Áfakulcs: EU - n kívüli
    VAT_EAM = 'EAM'

    # Áfakulcs: Mentes az adó alól
    VAT_NAM = 'KBAUK'

    # Áfakulcs: áfa tárgyi hatályán kívül
    VAT_ATK = 'ATK'

    # Áfakulcs: EU - n belüli
    VAT_EUFAD37 = 'EUFAD37'

    # Áfakulcs: EU - n belüli
    VAT_EUFADE = 'EUFADE'

    # Áfakulcs: EU - n belüli
    VAT_EUE = 'EUE'

    # Áfakulcs: EU - n kívüli
    VAT_HO = 'HO'

    # Alapértelmezett ÁFA érték
    DEFAULT_VAT = '27'

    # Alapértelmezett mennyiség
    DEFAULT_QUANTITY = 1.0

    # Alapértelmezett mennyiségi egység
    DEFAULT_QUANTITY_UNIT = 'db'

    def __init__(self, name, net_unit_price, quantity=DEFAULT_QUANTITY,
                 quantity_unit=DEFAULT_QUANTITY_UNIT, vat=DEFAULT_VAT):
        self.id = ""
        self.name = name
        self.quantity = quantity
        self.quantity_unit = quantity_unit
        self.net_unit_price = net_unit_price
        self.vat = vat
        self.price_gap_vat_base = 0
        self.net_price = 0
        self.vat_amount = 0
        self.gross_amount = 0
        self.comment = ""
        self.required_fields = {'name', 'quantity', 'quantityUnit',
                                'netUnitPrice', 'vat', 'netPrice', 'vatAmount', 'grossAmount'}

    def __check_field(self, field, value):
        if hasattr(self, field):
            required = True if field in self.required_fields else False
            if field == 'quantity' \
                    or field == 'netUnitPrice' \
                    or field == 'priceGapVatBase' \
                    or field == 'netPrice' \
                    or field == 'vatAmount' \
                    or field == 'grossAmount':
                SzamlaAgentUtil.check_float_field(field, value, required, type(self).__name__)
            elif field == 'name' \
                    or field == 'id' \
                    or field == 'quantityUnit' \
                    or field == 'vat' \
                    or field == 'comment':
                SzamlaAgentUtil.check_str_field(field, value, required, type(self).__name__)
        return value

    def __check_fields(self):
        fields = inspect.getmembers(Buyer, lambda a: not (inspect.isroutine(a)))
        fields = [a for a in fields if not (a[0].startswith('__') and a[0].endswith('__'))]
        for item in fields:
            self.__check_field(item[0], item[1])

