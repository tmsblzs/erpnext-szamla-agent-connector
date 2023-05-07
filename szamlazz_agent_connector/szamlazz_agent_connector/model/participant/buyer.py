from html import escape


class Buyer:

    def __init__(self, name="", zip_code="", city="", address=""):
        self.id = 0
        self.name = name
        self.country = ""
        self.zip_code = zip_code
        self.city = city
        self.address = address
        self.email = ""
        self.send_email = True
        self.tax_payer = ""
        self.tax_number = ""
        self.tax_number_EU = ""
        self.postal_name = ""
        self.postal_country = ""
        self.postal_zip = ""
        self.postal_city = ""
        self.postal_address = ""
        self.ledger_data = None
        self.signatory_name = ""
        self.phone = ""
        self.comment = ""
        self.ledger_data = None
        self.__required_fields = {}

