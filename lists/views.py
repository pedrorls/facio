from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError

from .models import Item, List
from .forms import ItemForm


def home_page(request):
    return render(request, 'home.html', {'form': ItemForm()})


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
    return redirect(lst)


def view_list(request, list_id):
    lst = List.objects.get(id=list_id)
    error = None
    if request.method == 'POST':
        try:
            item_text = request.POST['item_text']
            item = Item.objects.create(text=item_text, list=lst)
            item.full_clean()
            item.save()
            return redirect(lst)
        except ValidationError:
            error = 'You cannot have an empty list item'
    return render(request, 'list.html', {'list': lst, 'error': error})
