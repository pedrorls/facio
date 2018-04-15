from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from .models import Item, List
from .forms import ItemForm, ExistingListItemForm
User = get_user_model()


def home_page(request):
    return render(request, 'home.html', {'form': ItemForm()})


def new_list(request):
    form = ItemForm(data=request.POST)
    if form.is_valid():
        lst = List()
        lst.owner = request.user
        lst.save()
        form.save(for_list=lst)
        return redirect(lst)
    else:
        return render(request, 'home.html', {'form': form})


def view_list(request, list_id):
    lst = List.objects.get(id=list_id)
    form = ExistingListItemForm(for_list=lst)
    if request.method == 'POST':
        form = ExistingListItemForm(for_list=lst, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(lst)
    return render(request, 'list.html', {'list': lst, 'form': form})


def my_lists(request, email):
    owner = User.objects.get(email=email)
    return render(request, 'my_lists.html', {'owner': owner})
