from django.test import TestCase
from lists.models import Item, List


class HomePageTest(TestCase):
    def test_uses_home_template(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "home.html")  

    def test_renders_input_form(self):  
        response = self.client.get("/")
        self.assertContains(response, '<form method="POST" action="/lists/new">') 
        self.assertContains(response, '<input name="item_text"')
        self.assertContains(response, '<input name="item_priority"')

class NewListTest(TestCase):
    def test_can_save_a_POST_request(self):
        self.client.post("/lists/new", data={
            
            "item_text": "A new list item",
            "item_priority": "Low"
            
            })
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.get()
        self.assertEqual(new_item.text, "A new list item")
        self.assertEqual(new_item.priority, "Low")

    def test_redirects_after_POST(self):
        response = self.client.post("/lists/new", data={
            
            "item_text": "A new list item",
            "item_priority": "Low"
            
            })
        new_list = List.objects.get()
        self.assertRedirects(response, f"/lists/{new_list.id}/")



class ListViewTest(TestCase):
    def test_uses_list_template(self):
        mylist = List.objects.create()
        response = self.client.get(f"/lists/{mylist.id}/")  
        self.assertTemplateUsed(response, "list.html")

    def test_renders_input_form(self):
        mylist = List.objects.create()
        response = self.client.get(f"/lists/{mylist.id}/")
        self.assertContains(
            response,
            f'<form method="POST" action="/lists/{mylist.id}/add_item">',
        )
        self.assertContains(response, '<input name="item_text"')
        self.assertContains(response, '<input name="item_priority"')
        
    def test_displays_only_items_for_that_list(self):
        correct_list = List.objects.create()  
        Item.objects.create(text="itemey 1", priority="High", list=correct_list)
        Item.objects.create(text="itemey 2", priority="Low", list=correct_list)
        other_list = List.objects.create()  
        Item.objects.create(text="other list item", priority="Medium", list=other_list)

        response = self.client.get(f"/lists/{correct_list.id}/")  

        self.assertContains(response, "itemey 1 | Priority(High)")
        self.assertContains(response, "itemey 2 | Priority(Low)")
        self.assertContains(response, '<a class="btn-edit"')
        self.assertNotContains(response, "other list item | Priority(Medium)")  

class ListAndItemModelsTest(TestCase):
    def test_saving_and_retrieving_items(self):
        mylist = List()
        mylist.save()

        first_item = Item()
        first_item.text = "The first (ever) list item"
        first_item.priority = "Low"
        first_item.list = mylist
        first_item.save()

        second_item = Item()
        second_item.text = "Item the second"
        second_item.priority = "High"
        second_item.list = mylist
        second_item.save()

        saved_list = List.objects.get()
        self.assertEqual(saved_list, mylist)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, "The first (ever) list item")
        self.assertEqual(first_saved_item.priority, "Low")
        self.assertEqual(first_saved_item.list, mylist)
        self.assertEqual(second_saved_item.text, "Item the second")
        self.assertEqual(second_saved_item.priority, "High")
        self.assertEqual(second_saved_item.list, mylist)

class NewItemTest(TestCase):
    def test_can_save_a_POST_request_to_an_existing_list(self):
       
        correct_list = List.objects.create()

        self.client.post(
            f"/lists/{correct_list.id}/add_item",
            data={"item_text": "A new item for an existing list",
                  "item_priority": "Low"}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.get()
        self.assertEqual(new_item.text, "A new item for an existing list")
        self.assertEqual(new_item.list, correct_list)

    def test_redirects_to_list_view(self):
     
        correct_list = List.objects.create()

        response = self.client.post(
            f"/lists/{correct_list.id}/add_item",
            data={"item_text": "A new item for an existing list",
                  "item_priority": "Low"},
        )

        self.assertRedirects(response, f"/lists/{correct_list.id}/")

class EditViewTest(TestCase):

    # ดูว่าใช้ edit template ไหม
    def test_uses_edit_template(self):
        mylist = List.objects.create()
        item = Item.objects.create(text="edit me", priority="Low", list=mylist)
    
        response = self.client.get(f'/lists/{mylist.id}/edit/{item.id}/')
        self.assertTemplateUsed(response, 'edit.html')

    # ดูว่า edit template ขึ้นข้อมูลเดิมไหม
    def test_displays_item_data_in_form(self):

        mylist = List.objects.create()
        item = Item.objects.create(text="original text", priority="High", list=mylist)
        
        response = self.client.get(f'/lists/{mylist.id}/edit/{item.id}/')

        # ตรวจสอบว่ามีข้อมูลเดิมอยู่ใน attribute 'value' ของ input
        self.assertContains(response, 'value="original text"')
        self.assertContains(response, 'value="High"')

    # ดูว่ามันสามารถแก้ไขข้อมูลได้จริง
    def test_can_save_a_post_request_to_an_existing_item(self):

        mylist = List.objects.create()
        item = Item.objects.create(text="old text", priority="Low", list=mylist)

        # ส่งข้อมูลใหม่ไปที่ URL สำหรับแก้ไข
        self.client.post(
            f'/lists/{mylist.id}/edit/{item.id}/',
            data={'item_text': 'new text', 'item_priority': 'Urgent'}
        )

        # ดึงข้อมูลจาก DB มาเช็คว่าเปลี่ยนจริงไหม
        item.refresh_from_db()
        self.assertEqual(item.text, 'new text')
        self.assertEqual(item.priority, 'Urgent')

    # เมื่อแก้ไขเสร็จแล้ว redirect กลับไปหน้า lists ไหม
    def test_redirects_after_post(self):
    
        mylist = List.objects.create()
        item = Item.objects.create(text="old", priority="Low", list=mylist)

        response = self.client.post(
            f'/lists/{mylist.id}/edit/{item.id}/',
            data={'item_text': 'new', 'item_priority': 'High'}
        )
        self.assertRedirects(response, f'/lists/{mylist.id}/')

    