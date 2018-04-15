from django.conf import settings
from .base import FunctionalTest
from .server_tools import create_session_on_server
from .management.commands.create_session import (
    create_pre_authenticated_session
)


class MyListTest(FunctionalTest):

    def create_pre_authenticated_session(self, email):
        if self.staging_server:
            session_key = create_session_on_server(self.staging_server, email)
        else:
            session_key = create_pre_authenticated_session(email)

        self.browser.get(self.live_server_url + '/404/')
        self.browser.add_cookie(dict(
            name=settings.SESSION_COOKIE_NAME,
            value=session_key,
            path='/',
        ))

    def test_logged_in_pre_authemticated_users(self):
        email = 'edith@example.com'
        self.browser.get(self.live_server_url)
        self.wait_to_be_logged_out(email)

        self.create_pre_authenticated_session(email)
        self.browser.get(self.live_server_url)
        self.wait_to_be_logged_in(email)

    def test_logged_in_users_lists_are_saved_as_my_lists(self):
        email = 'edith@example.com'
        self.create_pre_authenticated_session(email)
        self.browser.get(self.live_server_url)
        self.insert_list_item('Reticulate splines')
        self.insert_list_item('Immanentize eschaton')
        first_lst_url = self.browser.current_url
        self.browser.find_element_by_link_text('My lists').click()

        self.wait_for(
            lambda: self.browser.find_element_by_link_text(
                'Reticulate splines'
            )

        )
        self.browser.find_element_by_link_text('Reticulate splines').click()
        self.wait_for(
            lambda: self.assertEqual(self.browser.current_url, first_lst_url)
        )

        self.browser.get(self.live_server_url)
        self.insert_list_item('Click cows')
        second_lst_url = self.browser.current_url

        self.browser.find_element_by_link_text('My lists').click()
        self.wait_for(
            lambda: self.browser.find_element_by_link_text('Click cows')
        )
        self.browser.find_element_by_link_text('Click cows').click()
        self.wait_for(
            lambda: self.assertEqual(self.browser.current_url, second_lst_url)
        )
        self.browser.find_element_by_link_text('Logout').click()
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_elements_by_link_text('My lists'), []
        ))
