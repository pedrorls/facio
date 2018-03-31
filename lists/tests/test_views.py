from django.test import TestCase
from django.urls import resolve

from ..views import home_page
from ..models import Item, List


class HomePageTests(TestCase):
    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')


class ListViewTest(TestCase):
    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.id}/')
        self.assertTemplateUsed(response, 'list.html')

    def test_display_all_list_items(self):
        correct_list = List.objects.create()
        Item.objects.create(text='Item 1', list=correct_list)
        Item.objects.create(text='Item 2', list=correct_list)
        wrong_list = List.objects.create()
        Item.objects.create(text='Another item 1', list=wrong_list)
        Item.objects.create(text='Another item 2', list=wrong_list)
        response = self.client.get(f'/lists/{correct_list.id}/')
        self.assertContains(response, 'Item 1')
        self.assertContains(response, 'Item 2')
        self.assertNotContains(response, 'Another item 1')
        self.assertNotContains(response, 'Another item 2')

    def test_passes_correct_list_to_template(self):
        other_lst = List.objects.create()
        correct_lst = List.objects.create()
        response = self.client.get(f'/lists/{correct_lst.id}/')
        self.assertEqual(response.context['list'], correct_lst)

    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_lst = List.objects.create()
        correct_lst = List.objects.create()

        self.client.post(
            f'/lists/{correct_lst.id}/',
            data={'item_text': 'A new list item for an existing list'}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item for an existing list')
        self.assertEqual(new_item.list, correct_lst)

    def test_POST_redirects_to_list_view(self):
        other_lst = List.objects.create()
        correct_lst = List.objects.create()
        response = self.client.post(
            f'/lists/{correct_lst.id}/',
            data={'item_text': 'A new list item for an existing list'}
        )
        self.assertRedirects(response, f'/lists/{correct_lst.id}/')


class NewListTest(TestCase):

    def test_validation_errors_are_sent_back_to_home_page_template(self):
        response = self.client.post('/lists/new', data={'item_text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        expected_error = 'You cannot have an empty list item'
        self.assertContains(response, expected_error)

    def test_invalid_list_items_aret_saved(self):
        self.client.post('/lists/new', data={'item_text': ''})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)
