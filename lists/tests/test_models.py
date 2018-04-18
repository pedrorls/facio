from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from ..models import Item, List
User = get_user_model()


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

    def test_cannot_save_empty_list(self):
        lst = List.objects.create()
        item = Item(list=lst, text='')
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()

    def test_get_absolute_url(self):
        lst = List.objects.create()
        self.assertEqual(lst.get_absolute_url(), f'/lists/{lst.id}/')

    def resr_create_new_creates_list_and_first_item(self):
        List.create_new(first_item_text='new item text')
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'new item text')
        new_lst = List.objects.first()
        self.assertEqual(new_item.list, new_lst)

    def test_create_new_optionally_saves_owner(self):
        user = User.objects.create()
        List.create_new(first_item_text='new item text', owner=user)
        lst = List.objects.first()
        self.assertEqual(lst.owner, user)

    def test_lists_can_have_owners(self):
        List(owner=User())  # Should not raise

    def test_list_owner_is_optional(self):
        List().full_clean()  # Should not raise

    def test_create_returns_new_list_objects(self):
        returned = List.create_new(first_item_text='new item text')
        lst = List.objects.first()
        self.assertEqual(returned, lst)

    def test_list_name_is_first_item_text(self):
        lst = List.objects.create()
        Item.objects.create(list=lst, text='first item')
        Item.objects.create(list=lst, text='second item')
        self.assertEqual(lst.name, 'first item')
