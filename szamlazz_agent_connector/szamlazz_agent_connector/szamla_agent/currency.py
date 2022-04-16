class Currency:
    CURRENCY_FT  = 'Ft'
    # forint
    CURRENCY_HUF = 'HUF'
    # euró
    CURRENCY_EUR = 'EUR'
    # svájci frank
    CURRENCY_CHF = 'CHF'
    # amerikai dollár
    CURRENCY_USD = 'USD'
    # Arab Emírségek dirham
    CURRENCY_AED = 'AED'
    # ausztrál dollár
    CURRENCY_AUD = 'AUD'
    # bolgár leva
    CURRENCY_BGN = 'BGN'
    # brazil real
    CURRENCY_BRL = 'BRL'
    # kanadai dollár
    CURRENCY_CAD = 'CAD'
    # kínai jüan
    CURRENCY_CNY = 'CNY'
    # cseh korona
    CURRENCY_CZK = 'CZK'
    # dán korona
    CURRENCY_DKK = 'DKK'
    # észt korona
    CURRENCY_EEK = 'EEK'
    # angol font
    CURRENCY_GBP = 'GBP'
    # hongkongi dollár
    CURRENCY_HKD = 'HKD'
    # horvát kún
    CURRENCY_HRK = 'HRK'
    # indonéz rúpia
    CURRENCY_IDR = 'IDR'
    # izraeli sékel
    CURRENCY_ILS = 'ILS'
    # indiai rúpia
    CURRENCY_INR = 'INR'
    # izlandi korona
    CURRENCY_ISK = 'ISK'
    # japán jen
    CURRENCY_JPY = 'JPY'
    # dél-koreai won
    CURRENCY_KRW = 'KRW'
    # litván litas
    CURRENCY_LTL = 'LTL'
    # lett lat
    CURRENCY_LVL = 'LVL'
    # mexikói peso
    CURRENCY_MXN = 'MXN'
    # maláj ringgit
    CURRENCY_MYR = 'MYR'
    # norvég koro
    CURRENCY_NOK = 'NOK'
    # új-zélandi dollár
    CURRENCY_NZD = 'NZD'
    # fülöp-szigeteki peso
    CURRENCY_PHP = 'PHP'
    # lengyel zloty
    CURRENCY_PLN = 'PLN'
    # új román lej
    CURRENCY_RON = 'RON'
    # szerb dínár
    CURRENCY_RSD = 'RSD'
    # orosz rubel
    CURRENCY_RUB = 'RUB'
    # svéd koron
    CURRENCY_SEK = 'SEK'
    # szingapúri dollár
    CURRENCY_SGD = 'SGD'
    # thai bát
    CURRENCY_THB = 'THB'
    # török líra
    CURRENCY_TRY = 'TRY'
    # ukrán hryvna
    CURRENCY_UAH = 'UAH'
    # vietnámi dong
    CURRENCY_VND = 'VND'
    # dél-afrikai rand
    CURRENCY_ZAR = 'ZAR'

    @staticmethod
    def get_default():
        return Currency.CURRENCY_FT
    
    @staticmethod
    def get_currency_str(currency):
        if currency is None or currency == '' or currency == "Ft" or currency == "HUF":
            result = "forint"
        else: 
            switcher = {
                'Currency.CURRENCY_EUR' : "euró",
                'Currency.CURRENCY_USD' : "amerikai dollár",
                'Currency.CURRENCY_AUD' : "ausztrál dollár",
                'Currency.CURRENCY_AED' : "Arab Emírségek dirham",
                'Currency.CURRENCY_BRL' : "brazil real",
                'Currency.CURRENCY_CAD' : "kanadai dollár",
                'Currency.CURRENCY_CHF' : "svájci frank",
                'Currency.CURRENCY_CNY' : "kínai jüan",
                'Currency.CURRENCY_CZK' : "cseh korona",
                'Currency.CURRENCY_DKK' : "dán korona",
                'Currency.CURRENCY_EEK' : "észt korona",
                'Currency.CURRENCY_GBP' : "angol font",
                'Currency.CURRENCY_HKD' : "hongkongi dollár",
                'Currency.CURRENCY_HRK' : "horvát kúna",
                'Currency.CURRENCY_ISK' : "izlandi korona",
                'Currency.CURRENCY_JPY' : "japán jen",
                'Currency.CURRENCY_LTL' : "litván litas",
                'Currency.CURRENCY_LVL' : "lett lat",
                'Currency.CURRENCY_MXN' : "mexikói peso",
                'Currency.CURRENCY_NOK' : "norvég koron",
                'Currency.CURRENCY_NZD' : "új-zélandi dollár",
                'Currency.CURRENCY_PLN' : "lengyel zloty",
                'Currency.CURRENCY_RON' : "új román lej",
                'Currency.CURRENCY_RUB' : "orosz rubel",
                'Currency.CURRENCY_SEK' : "svéd koron",
                'Currency.CURRENCY_UAH' : "ukrán hryvna",
                'Currency.CURRENCY_BGN' : "bolgár leva",
                'Currency.CURRENCY_RSD' : "szerb dínár",
                'Currency.CURRENCY_ILS' : "izraeli sékel",
                'Currency.CURRENCY_IDR' : "indonéz rúpia",
                'Currency.CURRENCY_INR' : "indiai rúpia",
                'Currency.CURRENCY_TRY' : "török líra",
                'Currency.CURRENCY_VND' : "vietnámi dong",
                'Currency.CURRENCY_SGD' : "szingapúri dollár",
                'Currency.CURRENCY_THB' : "thai bát",
                'Currency.CURRENCY_KRW' : "dél-koreai won",
                'Currency.CURRENCY_MYR' : "maláj ringgit",
                'Currency.CURRENCY_PHP' : "fülöp-szigeteki peso",
                'Currency.CURRENCY_ZAR' : "dél-afrikai rand"
            }
            result = switcher.get(currency, "ismeretlen")
        return result

