import unittest

from frappe.tests.utils import FrappeTestCase
from szamlazz_agent_connector.szamlazz_agent_connector.helper.address.shipping_address_helper import \
    ShippingAddressHelper


class TestShippingAddressHelper(FrappeTestCase):
    def test_replace_new_line_ch_to_emtpy(self):
        SHIPPING_ADDRESS = "test city \n test address"
        EXPECTED_ADDRESS = ShippingAddressHelper\
            .SHIPPING_ADDRESS_TEMPLATE\
            .format(SHIPPING_ADDRESS.replace('\n', ''))
        result = ShippingAddressHelper.format(SHIPPING_ADDRESS)

        self.assertEqual(result, EXPECTED_ADDRESS)

    def test_replace_break_to_new_line_ch(self):
        SHIPPING_ADDRESS = "test city <br> test address"
        EXPECTED_ADDRESS = ShippingAddressHelper\
            .SHIPPING_ADDRESS_TEMPLATE\
            .format(SHIPPING_ADDRESS.replace('<br>', '\n'))
        result = ShippingAddressHelper.format(SHIPPING_ADDRESS)

        self.assertEqual(result, EXPECTED_ADDRESS)

    def test_format_address_using_template(self):
        SHIPPING_ADDRESS = "test city test address"
        EXPECTED_ADDRESS = ShippingAddressHelper\
            .SHIPPING_ADDRESS_TEMPLATE\
            .format(SHIPPING_ADDRESS)
        result = ShippingAddressHelper.format(SHIPPING_ADDRESS)

        self.assertEqual(result, EXPECTED_ADDRESS)
