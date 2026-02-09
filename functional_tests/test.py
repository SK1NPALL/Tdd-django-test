
from django.test import LiveServerTestCase  # เปลี่ยนการ import
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

from selenium.common.exceptions import WebDriverException
MAX_WAIT = 5  

class NewVisitorTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()
    
    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:  
            try:
                table = self.browser.find_element(By.ID, "id_list_table")  
                rows = table.find_elements(By.TAG_NAME, "tr")
                self.assertIn(row_text, [row.text for row in rows])
                return  
            except (AssertionError, WebDriverException):  
                if time.time() - start_time > MAX_WAIT:  
                    raise  
                time.sleep(0.5)

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element(By.ID, "id_list_table")
        rows = table.find_elements(By.TAG_NAME, "tr")
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_todo_list(self):
        # Edith has heard about a cool new online to-do app.
        # She goes to check out its homepage
        self.browser.get("http://localhost:8000")

        # She notices the page title and header mention to-do lists
        self.assertIn("To-Do", self.browser.title)
        header_text = self.browser.find_element(By.TAG_NAME, "h1").text  
        self.assertIn("To-Do", header_text)

        # She is invited to enter a to-do item straight away
        inputbox = self.browser.find_element(By.ID, "id_new_item")  
        self.assertEqual(inputbox.get_attribute("placeholder"), "Enter a to-do item")

        self.browser.get(self.live_server_url) 
        
        # เพิ่มรายการแรก: Buy peacock feathers | Priority(High)
        inputbox = self.browser.find_element(By.ID, "id_new_item")
        inputbox.send_keys("Buy peacock feathers")
        inputbox_priority = self.browser.find_element(By.ID, "id_new_item_priority")
        inputbox_priority.send_keys("High")
        inputbox_priority.send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table("1: Buy peacock feathers | Priority(High) Edit")

        time.sleep(1)  # สั่งให้ Python หยุดรอ 1 วินาที เพื่อให้หน้าจอโหลดเสร็จ
        edit_button = self.browser.find_element(By.CLASS_NAME, "edit-button")
        edit_button.click()

        # แก้ไขจาก Buy peacock feathers (High) -> Buy penguin feathers (Low)
        inputbox = self.browser.find_element(By.ID, "id_new_item")
        inputbox.clear() 
        inputbox.send_keys("Buy penguin feathers")
        inputbox_priority = self.browser.find_element(By.ID, "id_new_item_priority")
        inputbox_priority.clear()
        inputbox_priority.send_keys("Low")
        inputbox_priority.send_keys(Keys.ENTER)

        # ตรวจสอบว่ารายการที่ 1 กลายเป็นของใหม่แล้ว
        self.wait_for_row_in_list_table("1: Buy penguin feathers | Priority(Low) Edit")
        
        # --- ส่วนการเพิ่มรายการที่สอง ---
        inputbox = self.browser.find_element(By.ID, "id_new_item")
        inputbox.send_keys("Use peacock feathers to make a fly")
        inputbox_priority = self.browser.find_element(By.ID, "id_new_item_priority")  
        inputbox_priority.send_keys("Low")
        inputbox_priority.send_keys(Keys.ENTER)

        # ตรวจสอบรายการทั้งหมดที่ควรจะมีอยู่ในหน้าปัจจุบัน
        # รายการที่ 2 คือที่เพิ่งเพิ่มใหม่
        self.wait_for_row_in_list_table("2: Use peacock feathers to make a fly | Priority(Low) Edit")
        
        # รายการที่ 1 ต้องเป็น "Buy penguin feathers" (เพราะเราเพิ่ง Edit ไปข้างบน)
        self.wait_for_row_in_list_table("1: Buy penguin feathers | Priority(Low) Edit")

        # Satisfied, she goes back to sleep
    def test_multiple_users_can_start_lists_at_different_urls(self):
        # Edith starts a new to-do list
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element(By.ID, "id_new_item")
        inputbox.send_keys("Buy peacock feathers")

        inputbox_priority = self.browser.find_element(By.ID, "id_new_item_priority")
        inputbox_priority.send_keys("Medium")

        inputbox_priority.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Buy peacock feathers | Priority(Medium) Edit")

        # She notices that her list has a unique URL
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, "/lists/.+")

        # Now a new user, Francis, comes along to the site.

        ## We delete all the browser's cookies
        ## as a way of simulating a brand new user session  
        self.browser.delete_all_cookies()

        # Francis visits the home page.  There is no sign of Edith's
        # list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element(By.TAG_NAME, "body").text
        self.assertNotIn("Buy peacock feathers | Priority(Medium)", page_text)

        # Francis starts a new list by entering a new item. He
        # is less interesting than Edith...
        inputbox = self.browser.find_element(By.ID, "id_new_item")
        inputbox.send_keys("Buy milk")

        inputbox_priority = self.browser.find_element(By.ID, "id_new_item_priority")
        inputbox_priority.send_keys("High")

        inputbox_priority.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Buy milk | Priority(High) Edit")

        # Francis gets his own unique URL
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, "/lists/.+")
        self.assertNotEqual(francis_list_url, edith_list_url)

        # Again, there is no trace of Edith's list
        page_text = self.browser.find_element(By.TAG_NAME, "body").text
        self.assertNotIn("Buy peacock feathers | Priority(Medium)", page_text)
        self.assertIn("Buy milk | Priority(High)", page_text)

        # Satisfied, they both go back to sleep

        
