
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

        # She types "Buy peacock feathers" into a text box
        # (Edith's hobby is tying fly-fishing lures)
        inputbox.send_keys("Buy peacock feathers") 

        # She find the priority box
        inputbox_priority = self.browser.find_element(By.ID, "id_new_item_priority")  
        self.assertEqual(inputbox_priority.get_attribute("placeholder"), "Enter a priority")

        # She types "High" into a priority box
        inputbox_priority.send_keys("High") 

        # When she hits enter, the page updates, and now the page lists
        # "1: Buy peacock feathers" as an item in a to-do list table
        inputbox_priority.send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table("1: Buy peacock feathers | Priority(High)")

        # เธอเห็นปุ่มแก้ไขขึ้นอยู่ที่ข้างๆ list ที่ถูกพิ่มเข้าไป
        edit_button = self.browser.find_element(By.CLASS_NAME, "bit-edit")
        edit_button.click()

        # เธอถูกส่งไปหน้าแก้ไข ซึ่งมีข้อมูลเดิมอยู่แล้ว
        # ตรวจสอบว่า input box มีค่าเดิม อยู่หรือไม่
        inputbox = self.browser.find_element(By.ID, "id_new_item")
        self.assertEqual(inputbox.get_attribute("value"), "Buy peacock feathers")

        inputbox_priority = self.browser.find_element(By.ID, "id_new_item_priority")
        self.assertEqual(inputbox_priority.get_attribute("value"), "High")

        # เธอเปลี่ยนข้อความจาก "Buy peacock feathers" เป็น "Buy many peacock feathers"
        # และเปลี่ยน Priority จาก High เป็น Low
        inputbox.clear() 
        inputbox.send_keys("Buy penguin feathers")

        inputbox_priority = self.browser.find_element(By.ID, "id_new_item_priority")
        inputbox_priority.clear()
        inputbox_priority.send_keys("Low")
        inputbox_priority.send_keys(Keys.ENTER)

        # หน้าจอพากลับมาที่หน้ารายการ และแสดงข้อมูลที่แก้ไขแล้ว
        self.wait_for_row_in_list_table("1: Buy penguin feathers | Priority(Low)")
        
        # ตรวจสอบว่าข้อมูลเก่าหายไปแล้ว
        page_text = self.browser.find_element(By.TAG_NAME, "body").text
        self.assertNotIn("Buy peacock feathers | Priority(High)", page_text)

        # There is still a text box inviting her to add another item.
        # She enters "Use peacock feathers to make a fly"
        # (Edith is very methodical)
        inputbox = self.browser.find_element(By.ID, "id_new_item")
        inputbox.send_keys("Use peacock feathers to make a fly")

        inputbox_priority = self.browser.find_element(By.ID, "id_new_item_priority")  
        inputbox_priority.send_keys("Low")

        inputbox_priority.send_keys(Keys.ENTER)

        # The page updates again, and now shows both items on her list
        self.wait_for_row_in_list_table("2: Use peacock feathers to make a fly | Priority(Low)")
        self.wait_for_row_in_list_table("1: Buy peacock feathers | Priority(High)")

         # Satisfied, she goes back to sleep

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # Edith starts a new to-do list
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element(By.ID, "id_new_item")
        inputbox.send_keys("Buy peacock feathers")

        inputbox_priority = self.browser.find_element(By.ID, "id_new_item_priority")
        inputbox_priority.send_keys("Medium")

        inputbox_priority.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Buy peacock feathers | Priority(Medium)")

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
        self.wait_for_row_in_list_table("1: Buy milk | Priority(High)")

        # Francis gets his own unique URL
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, "/lists/.+")
        self.assertNotEqual(francis_list_url, edith_list_url)

        # Again, there is no trace of Edith's list
        page_text = self.browser.find_element(By.TAG_NAME, "body").text
        self.assertNotIn("Buy peacock feathers | Priority(Medium)", page_text)
        self.assertIn("Buy milk | Priority(High)", page_text)

        # Satisfied, they both go back to sleep

        
