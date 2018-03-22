from django.shortcuts import render, redirect

from .models import Item

def home_page(request):
    if request.method == 'POST':
        new_item = request.POST['item_text']
        Item.objects.create(text=new_item)
        return redirect('/')
    items = Item.objects.all()
    return render(request, 'home.html', {'items': items})