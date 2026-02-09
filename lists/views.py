from django.shortcuts import redirect , render 
from django.http import HttpResponse
from lists.models import Item , List

# Create your views here.

def home_page(request):
    
    return render(request, "home.html")

def about_page(request) :
    return render(request , "about.html")

def new_list(request):
    nulist = List.objects.create()
    Item.objects.create(text=request.POST["item_text"],
                        priority=request.POST["item_priority"],
                        list=nulist)
    return redirect(f"/lists/{nulist.id}/")

def view_list(request, list_id):
    our_list = List.objects.get(id=list_id)
    return render(request, "list.html", {"list": our_list})

def add_item(request, list_id):
    our_list = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST["item_text"],
                        priority=request.POST["item_priority"],
                        list=our_list)
    return redirect(f"/lists/{our_list.id}/")

def edit_item(request, list_id, item_id):
    our_list = List.objects.get(id=list_id)
    item = Item.objects.get(id=item_id)

    if request.method == "POST":
        item.text = request.POST["item_text"]
        item.priority = request.POST["item_priority"]
        item.save()
        return redirect(f"/lists/{our_list.id}/")

    return render(request, "edit.html", {"item": item, "list": our_list})
    

    

    