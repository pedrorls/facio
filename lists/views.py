from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError

from .models import Item, List


def home_page(request):
    return render(request, 'home.html')


def new_list(request):
    lst = List.objects.create()
    item = Item.objects.create(text=request.POST['item_text'], list=lst)
    try:
        item.full_clean()
        item.save()
    except ValidationError:
        lst.delete()
        error = 'You cannot have an empty list item'
        return render(request, 'home.html', {'error': error})
    return redirect(f'/lists/{lst.id}/')


def view_list(request, list_id):
    lst = List.objects.get(id=list_id)
    return render(request, 'list.html', {'list': lst})


def add_item(request, lst_id):
    lst = List.objects.get(id=lst_id)
    Item.objects.create(text=request.POST['item_text'], list=lst)
    return redirect(f'/lists/{lst.id}/')
