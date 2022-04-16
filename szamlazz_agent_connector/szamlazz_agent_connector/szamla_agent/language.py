class Language:
    LANGUAGE_HU = 'hu'
    LANGUAGE_EN = 'en'
    LANGUAGE_DE = 'de'
    LANGUAGE_IT = 'it'
    LANGUAGE_RO = 'ro'
    LANGUAGE_SK = 'sk'
    LANGUAGE_HR = 'hr'
    LANGUAGE_FR = 'fr'
    LANGUAGE_ES = 'es'
    LANGUAGE_CZ = 'cz'
    LANGUAGE_PL = 'pl'

    availableLanguages = [
        LANGUAGE_HU, 
        LANGUAGE_EN, 
        LANGUAGE_DE, 
        LANGUAGE_IT,
        LANGUAGE_RO, 
        LANGUAGE_SK, 
        LANGUAGE_HR, 
        LANGUAGE_FR,
        LANGUAGE_ES, 
        LANGUAGE_CZ, 
        LANGUAGE_PL
    ]

    @staticmethod
    def get_default():
        return Language.LANGUAGE_HU

    @staticmethod    
    def get_all():
        return Language.availableLanguages
    
    @staticmethod
    def get_language_str(language):
        if language is None and language == '' and language == Language.LANGUAGE_HU:
            result = "magyar"
        else:
            switcher = {
                Language.LANGUAGE_EN: "angol",
                Language.LANGUAGE_DE: "német",
                Language.LANGUAGE_IT: "olasz",
                Language.LANGUAGE_RO: "román",
                Language.LANGUAGE_SK: "szlovák",
                Language.LANGUAGE_HR: "horvát",
                Language.LANGUAGE_FR: "francia",
                Language.LANGUAGE_ES: "spanyol",
                Language.LANGUAGE_CZ: "cseh",
                Language.LANGUAGE_PL: "lengyel"
            }
            result = switcher.get(language, "ismeretlen")
        return result
    
    def get_available_languages(self):
        return self.availableLanguages
