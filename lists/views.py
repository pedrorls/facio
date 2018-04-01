from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError

from .models import Item, List
from .forms import ItemForm


def home_page(request):
    return render(request, 'home.html', {'form': ItemForm()})


def new_list(request):
    form = ItemForm(data=request.POST)
    if form.is_valid():
        lst = List.objects.create()
        form.save(for_list=lst)
        return redirect(lst)
    else:
        return render(request, 'home.html', {'form': form})


def view_list(request, list_id):
    lst = List.objects.get(id=list_id)
    form = ItemForm()
    if request.method == 'POST':
        form = ItemForm(data=request.POST)
        if form.is_valid():
            form.save(for_list=lst)
            return redirect(lst)
    return render(request, 'list.html', {'list': lst, 'form': form})
