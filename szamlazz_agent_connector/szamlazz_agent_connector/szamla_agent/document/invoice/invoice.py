class Invoice:

    # Számla típus: papír számla 
    INVOICE_TYPE_P_INVOICE = 1

    # Számla típus: e-számla 
    INVOICE_TYPE_E_INVOICE = 2

    # Számla lekérdezése számlaszám alapján 
    FROM_INVOICE_NUMBER = 1

    # Számla lekérdezése rendelési szám alapján 
    FROM_ORDER_NUMBER = 2

    # Jóváírások maximális száma
    # a számla kifizetettségének beállításakor
    CREDIT_NOTES_LIMIT = 5

    # Számlához csatolandó fájlok maximális száma 
    INVOICE_ATTACHMENTS_LIMIT = 5

    # Számlázz.hu ajánlott számlakép 
    INVOICE_TEMPLATE_DEFAULT = 'SzlaMost'

    # Tradicionális számlakép 
    INVOICE_TEMPLATE_TRADITIONAL = 'SzlaAlap'

    # Borítékbarát számlakép 
    INVOICE_TEMPLATE_ENV_FRIENDLY = 'SzlaNoEnv'

    # Hőnyomtatós számlakép (8 cm széles) 
    INVOICE_TEMPLATE_8CM = 'Szla8cm'

    # Retró kéziszámla számlakép 
    INVOICE_TEMPLATE_RETRO = 'SzlaTomb'

