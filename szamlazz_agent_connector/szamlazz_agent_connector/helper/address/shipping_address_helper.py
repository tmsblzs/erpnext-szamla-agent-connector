class ShippingAddressHelper:
    SHIPPING_ADDRESS_TEMPLATE = "Szállítási cím: \n{0}\n"

    @staticmethod
    def format(shipping_address):
        shipping_address = shipping_address.replace('\n', '')
        shipping_address = shipping_address.replace('<br>', '\n')
        return ShippingAddressHelper.SHIPPING_ADDRESS_TEMPLATE.format(shipping_address)
