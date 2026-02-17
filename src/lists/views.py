from django.shortcuts import redirect , render
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from lists.models import Item , List

# Create your views here.

def home_page(request):
    
    return render(request, "home.html")

def about_page(request) :
    return render(request , "about.html")

def new_list(request):
    list_ = List.objects.create()
    item = Item(list=list_, text=request.POST['item_text'])

    try:
        item.full_clean() # 1. สั่งให้ตรวจสอบกฎ (ห้ามว่าง)
        item.save()       # 2. ถ้าผ่าน ให้เซฟ
    except ValidationError:
        list_.delete()    # 3. ถ้าไม่ผ่าน ลบ List ที่เผลอสร้างไว้ทิ้งซะ
        error = "You can't have an empty list item"
        return render(request, 'home.html', {"error": error})

    return redirect(f"/lists/{list_.id}/")

def view_list(request, list_id):
    our_list = List.objects.get(id=list_id)
    return render(request, "list.html", {"list": our_list})

def add_item(request, list_id):
    list_ = List.objects.get(id=list_id)
    item = Item(list=list_, text=request.POST['item_text'])
    try:
        item.full_clean()
        item.save()
    except ValidationError:
        error = "You can't have an empty list item"
        return render(request, 'list.html', {"list": list_, "error": error})
        
    return redirect(f'/lists/{list_.id}/')
    

    