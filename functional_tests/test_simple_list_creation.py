from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest
import time


class NewVisitorTest(FunctionalTest):

    def test_can_start_a_list_and_retrieve_it_later(self):
        self.browser.get(self.live_server_url)
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)
        self.insert_list_item('Buy peacock feathers')
        time.sleep(0.5)
        self.insert_list_item('Use peacock feathers to make a fly')
        time.sleep(0.5)
        self.wait_for_row_in_list_table('1: Buy peacock feathers')
        self.wait_for_row_in_list_table(
            '2: Use peacock feathers to make a fly')

    def test_multiple_users_can_start_lists_at_different_urls(self):
        self.browser.get(self.live_server_url)
        self.insert_list_item('Buy peacock feathers')
        time.sleep(0.5)
        self.wait_for_row_in_list_table('1: Buy peacock feathers')
        list_url = self.browser.current_url
        self.assertRegex(list_url, '/lists/.+')
        # ------------------------------------------
        # quit browser session and open a new on to make sure
        # that no information of the other list is showed
        self.browser.quit()
        self.browser = webdriver.Chrome()

        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('Use peacock feathers to make a fly', page_text)

        self.insert_list_item('Buy milk')
        time.sleep(0.5)

        self.wait_for_row_in_list_table('1: Buy milk')
        other_list_url = self.browser.current_url
        tr_text = self.browser.find_element_by_tag_name('tr').text
        self.assertRegex(other_list_url, '/lists/.+')
        self.assertIn('Buy milk', tr_text)
