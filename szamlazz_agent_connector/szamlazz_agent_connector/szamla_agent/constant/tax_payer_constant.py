class TaxPayerConstant:
    # EU - n kívüli vállalkozás
    TAXPAYER_NON_EU_ENTERPRISE = 7

    # EU - s vállalkozás
    TAXPAYER_EU_ENTERPRISE = 6

    # Társas vállalkozás(Bt., Kft., zRt.)
    # Ne használd, helyette használd ezt: TaxPayer::TAXPAYER_HAS_TAXNUMBER.
    # deprecated
    TAXPAYER_JOINT_VENTURE = 5

    # Egyéni vállalkozó
    # Ne használd, helyette használd ezt: TaxPayer::TAXPAYER_HAS_TAXNUMBER.
    # deprecated
    TAXPAYER_INDIVIDUAL_BUSINESS = 4

    # Adószámos magánszemély
    # Ne használd, helyette használd ezt: TaxPayer::TAXPAYER_HAS_TAXNUMBER.
    # deprecated
    TAXPAYER_PRIVATE_INDIVIDUAL_WITH_TAXNUMBER = 3

    # Adószámos egyéb szervezet
    # Ne használd, helyette használd ezt: TaxPayer::TAXPAYER_HAS_TAXNUMBER.
    # deprecated
    TAXPAYER_OTHER_ORGANIZATION_WITH_TAXNUMBER = 2

    # Van magyar adószáma
    TAXPAYER_HAS_TAXNUMBER = 1

    # Nem tudjuk, hogy adóalany - e
    TAXPAYER_WE_DONT_KNOW = 0

    # Nincs adószáma
    TAXPAYER_NO_TAXNUMBER = -1

    # Magánszemély
    # Ne használd, helyette használd ezt: TaxPayer::TAXPAYER_NO_TAXNUMBER.
    # deprecated
    TAXPAYER_PRIVATE_INDIVIDUAL = -2

    # Adószám nélküli egyéb szervezet
    # Ne használd, helyette használd ezt: TaxPayer::TAXPAYER_NO_TAXNUMBER.
    # deprecated
    TAXPAYER_OTHER_ORGANIZATION_WITHOUT_TAXNUMBER = -3
