from django.test import TestCase
from django.core.exceptions import ValidationError

from ..models import Item, List


class ItemModelTest(TestCase):

    def test_default_text(self):
        item = Item()
        self.assertEqual(item.text, '')

    def test_item_is_related_to_list(self):
        lst = List.objects.create()
        item = Item()
        item.list = lst
        item.save()
        self.assertIn(item, lst.item_set.all())

    def test_duplicate_items_are_invalid(self):
        lst = List.objects.create()
        Item.objects.create(text='Douh', list=lst)
        with self.assertRaises(ValidationError):
            item = Item(text='Douh', list=lst)
            item.full_clean()

    def test_can_save_same_item_to_different_lists(self):
        lst1 = List.objects.create()
        lst2 = List.objects.create()
        Item.objects.create(text='Douh', list=lst1)
        item = Item(text='Douh', list=lst2)
        item.full_clean()  # Should not raise

    def test_list_ordering(self):
        lst = List.objects.create()
        item1 = Item.objects.create(text='item1', list=lst)
        item2 = Item.objects.create(text='item2', list=lst)
        item3 = Item.objects.create(text='item3', list=lst)
        self.assertEqual(
            list(Item.objects.all()),
            [item1, item2, item3]
        )

    def test_string_representation(self):
        item = Item(text='text')
        self.assertEqual(str(item), 'text')


class ListModelTest(TestCase):

    def test_get_absolute_url(self):
        lst = List.objects.create()
        self.assertEqual(lst.get_absolute_url(), f'/lists/{lst.id}/')

    def test_cannot_save_empty_list(self):
        lst = List.objects.create()
        item = Item(list=lst, text='')
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()
