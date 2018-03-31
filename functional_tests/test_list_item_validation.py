from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):
    def test_cannot_add_empty_list_items(self):
        self.browser.get(self.live_server_url)
        self.inset_list_item()
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_css_selector('.has-error').text,
            'You cannot have an empty list item'
        ))
        self.inset_list_item('Buy milk')
        self.wait_for_row_in_list_table('1: Buy milk')
        self.inset_list_item()
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_css_selector('.has-error').text,
            'You cannot have an empty list item'
        ))
        self.inset_list_item('Make tea')
        self.wait_for_row_in_list_table('1: Buy milk')
        self.wait_for_row_in_list_table('2: Make tea')
