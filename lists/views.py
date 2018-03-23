from django.shortcuts import render, redirect

from .models import Item, List

def home_page(request):
    return render(request, 'home.html')

def new_list(request):
    lst = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list=lst)
    return redirect(f'/lists/{lst.id}/')

def view_list(request, list_id):
    lst = List.objects.get(id=list_id)
    items = Item.objects.filter(list=lst)
    return render(request, 'list.html', {'items': items})
