from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):

    def get_error_element(self):
        return self.browser.find_element_by_css_selector('.has-danger')

    def test_cannot_add_empty_list_items(self):
        self.browser.get(self.live_server_url)
        self.insert_list_item()
        self.wait_for(lambda: self.browser.find_element_by_css_selector(
            '#id_text:invalid'
        ))
        self.get_item_input_box().send_keys('Buy milk')
        self.wait_for(lambda: self.browser.find_element_by_css_selector(
            '#id_text:valid'
        ))
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')
        self.wait_for(lambda: self.browser.find_element_by_css_selector(
            '#id_text:invalid'
        ))

        self.get_item_input_box().send_keys('Make tea')
        self.wait_for(lambda: self.browser.find_element_by_css_selector(
            '#id_text:valid'
        ))
        self.get_item_input_box().send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table('1: Buy milk')
        self.wait_for_row_in_list_table('2: Make tea')

    def test_cannot_add_duplicated_item(self):
        self.browser.get(self.live_server_url)
        self.insert_list_item('Buy wellies')
        self.wait_for_row_in_list_table('1: Buy wellies')
        self.insert_list_item('Buy wellies')

        self.wait_for(lambda: self.assertEqual(
            self.get_error_element().text,
            'You have already got this item in your list'
        ))

    def test_error_messages_are_cleared_on_input(self):
        self.browser.get(self.live_server_url)
        self.insert_list_item('Banter too thick')
        self.wait_for_row_in_list_table('1: Banter too thick')
        self.insert_list_item('Banter too thick')
        self.wait_for(lambda: self.assertTrue(
            self.get_error_element().is_displayed()
        ))
        self.get_item_input_box().send_keys('a')

        self.wait_for(lambda: self.assertFalse(
            self.get_error_element().is_displayed()
        ))
