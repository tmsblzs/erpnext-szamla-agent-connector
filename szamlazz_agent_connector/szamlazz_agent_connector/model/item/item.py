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
