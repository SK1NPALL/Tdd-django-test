[1mdiff --git a/functional_test.py b/functional_test.py[m
[1mindex e8b2038..aca586a 100644[m
[1m--- a/functional_test.py[m
[1m+++ b/functional_test.py[m
[36m@@ -1,29 +1,48 @@[m
[31m-import unittest[m
 from selenium import webdriver[m
[32m+[m[32mfrom selenium.webdriver.common.by import By[m
[32m+[m[32mfrom selenium.webdriver.common.keys import Keys[m
[32m+[m[32mimport time[m
[32m+[m[32mimport unittest[m
 [m
 [m
[31m-class NewVisitorTest(unittest.TestCase):  [m
[31m-    def setUp(self):  [m
[31m-        self.browser = webdriver.Chrome()  [m
[32m+[m[32mclass NewVisitorTest(unittest.TestCase):[m
[32m+[m[32m    def setUp(self):[m
[32m+[m[32m        self.browser = webdriver.Chrome()[m
 [m
[31m-    def tearDown(self):  [m
[32m+[m[32m    def tearDown(self):[m
         self.browser.quit()[m
 [m
[31m-    def test_can_start_a_todo_list(self):  [m
[32m+[m[32m    def test_can_start_a_todo_list(self):[m
         # Edith has heard about a cool new online to-do app.[m
         # She goes to check out its homepage[m
[31m-        self.browser.get("http://localhost:8000")  [m
[32m+[m[32m        self.browser.get("http://localhost:8000")[m
 [m
         # She notices the page title and header mention to-do lists[m
[31m-        self.assertIn("To-Do", self.browser.title)  [m
[32m+[m[32m        self.assertIn("To-Do", self.browser.title)[m
[32m+[m[32m        header_text = self.browser.find_element(By.TAG_NAME, "h1").text[m[41m  [m
[32m+[m[32m        self.assertIn("To-Do", header_text)[m
 [m
         # She is invited to enter a to-do item straight away[m
[31m-        self.fail("Finish the test!")  [m
[32m+[m[32m        inputbox = self.browser.find_element(By.ID, "id_new_item")[m[41m  [m
[32m+[m[32m        self.assertEqual(inputbox.get_attribute("placeholder"), "Enter a to-do item")[m
[32m+[m
[32m+[m[32m        # She types "Buy peacock feathers" into a text box[m
[32m+[m[32m        # (Edith's hobby is tying fly-fishing lures)[m
[32m+[m[32m        inputbox.send_keys("Buy peacock feathers")[m[41m  [m
 [m
[31m-        [...][m
[32m+[m[32m        # When she hits enter, the page updates, and now the page lists[m
[32m+[m[32m        # "1: Buy peacock feathers" as an item in a to-do list table[m
[32m+[m[32m        inputbox.send_keys(Keys.ENTER)[m[41m  [m
[32m+[m[32m        time.sleep(1)[m[41m  [m
 [m
[31m-        # Satisfied, she goes back to sleep[m
[32m+[m[32m        table = self.browser.find_element(By.ID, "id_list_table")[m
[32m+[m[32m        rows = table.find_elements(By.TAG_NAME, "tr")[m[41m  [m
[32m+[m[32m        self.assertTrue(any(row.text == "1: Buy peacock feathers" for row in rows))[m
 [m
[32m+[m[32m        # There is still a text box inviting her to add another item.[m
[32m+[m[32m        # She enters "Use peacock feathers to make a fly"[m
[32m+[m[32m        # (Edith is very methodical)[m
[32m+[m[32m        self.fail("Finish the test!")[m
 [m
[31m-if __name__ == "__main__":  [m
[31m-    unittest.main()  [m
\ No newline at end of file[m
[32m+[m[32m        # The page updates again, and now shows both items on her list[m
[32m+[m[32m        [...][m
\ No newline at end of file[m
