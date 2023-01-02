from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import unittest 
import HtmlTestRunner
import time 

class GreenCartTest(unittest.TestCase):

    def setUp(self):
        chr_options = Options()
        chr_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chr_options)
        self.driver.implicitly_wait(10)
        self.driver.maximize_window()
        self.driver.get("https://rahulshettyacademy.com/seleniumPractise/#/")

    def test_add_item(self):
        self.add_button = self.driver.find_element(By.XPATH, "//div[@class='products']//div[1]//div[3]//button[1]")
        for i in range(2):
            self.driver.find_element(By.XPATH, '//*[@id="root"]/div/div[1]/div/div[1]/div[2]/a[2]').click()
        self.add_button.click()
        self.actual_item_num = int(self.driver.find_element(By.XPATH, '//*[@id="root"]/div/header/div/div[3]/div[1]/table/tbody/tr[1]/td[3]/strong').text)
        self.actual_item_price = int(self.driver.find_element(By.XPATH, '//*[@id="root"]/div/header/div/div[3]/div[1]/table/tbody/tr[2]/td[3]/strong').text)
        self.assertEqual(self.actual_item_num, 1) and self.assertEqual(self.actual_item_price, 3 * 120)
    
    def test_items_present_after_refresh(self):
        self.add_button = self.driver.find_element(By.XPATH, "//div[@class='products']//div[1]//div[3]//button[1]")
        self.add_button.click()
        self.actual_item_num = int(self.driver.find_element(By.XPATH, '//*[@id="root"]/div/header/div/div[3]/div[1]/table/tbody/tr[1]/td[3]/strong').text)
        self.actual_item_price = int(self.driver.find_element(By.XPATH, '//*[@id="root"]/div/header/div/div[3]/div[1]/table/tbody/tr[2]/td[3]/strong').text)
        self.driver.refresh()
        self.assertEqual(self.actual_item_num, int(self.driver.find_element(By.XPATH, '//*[@id="root"]/div/header/div/div[3]/div[1]/table/tbody/tr[1]/td[3]/strong').text))
        self.assertEqual(self.actual_item_price, int(self.driver.find_element(By.XPATH, '//*[@id="root"]/div/header/div/div[3]/div[1]/table/tbody/tr[2]/td[3]/strong').text))

    def test_add_button_change(self):
        self.add_button = self.driver.find_element(By.XPATH, "//div[@class='products']//div[1]//div[3]//button[1]")
        self.add_button.click()
        self.assertEqual(self.add_button.text, "✔ ADDED")
        
    def test_sum_total(self):
        self.driver.find_element(By.XPATH, "//div[@class='products']//div[1]//div[3]//button[1]").click()
        self.driver.find_element(By.XPATH, "/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[6]/div[3]/button[1]").click()
        self.driver.find_element(By.XPATH, "/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[7]/div[3]/button[1]").click()
        self.actual_item_num = int(self.driver.find_element(By.XPATH, '//*[@id="root"]/div/header/div/div[3]/div[1]/table/tbody/tr[1]/td[3]/strong').text)
        self.assertEqual(self.actual_item_num, 3)
    
    def test_remove_item(self):
        for i in range(3):
            self.driver.find_element(By.XPATH, "/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[4]/div[3]/button[1]").click()
        self.driver.find_element(By.XPATH, "//img[@alt='Cart']").click()
        self.driver.find_element(By.XPATH, "//div[@class='cart-preview active']//div//div//a[@class='product-remove'][normalize-space()='×']").click()
        self.assertEqual(self.driver.find_element(By.XPATH, "//div[@class='cart-preview active']//div//div//h2[contains(text(),'You cart is empty!')]").text, "Your cart is empty!")

    def test_button_disabled(self):
        self.driver.find_element(By.XPATH, "//img[@alt='Cart']").click()
        self.checkout = self.driver.find_element(By.XPATH, "//button[normalize-space()='PROCEED TO CHECKOUT']")
        self.assert_(self.checkout.is_enabled() == False)
    
    def test_logo_displayed(self):
        self.logo = self.driver.find_element(By.XPATH, "//div[@class='brand greenLogo']")
        self.assertTrue(self.logo.is_displayed() == True)

    def test_search(self):
        self.search_bar = self.driver.find_element(By.XPATH, "//input[@placeholder='Search for Vegetables and Fruits']")
        self.search_bar.send_keys("Brocolli")
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()
        self.products = self.driver.find_elements(By.XPATH, "//div[@class='product']")
        self.assertTrue(len(self.products) == 1 and "Brocolli" in self.products[0].text)

    def test_search_noresult(self):
        self.search_bar = self.driver.find_element(By.XPATH, "//input[@placeholder='Search for Vegetables and Fruits']")
        self.search_bar.send_keys("123")
        self.noResult = self.driver.find_element(By.XPATH, "(//div[@class='no-results'])[1]")
        self.assertTrue(self.noResult.is_displayed())

    def test_navigate_link(self):
        self.driver.find_element(By.LINK_TEXT, 'Top Deals').click()
        current_window = self.driver.current_window_handle
        #get first child window
        child_window = self.driver.window_handles
        for w in child_window:
        #switch focus to child window
            if (w != current_window):
                self.driver.switch_to.window(w)
        print(self.driver.current_url)
        self.assertTrue(self.driver.current_url == 'https://rahulshettyacademy.com/seleniumPractise/#/offers')

    def tearDown(self):
        self.driver.close()
        self.driver.quit()
        print("Test Completed")

if __name__ == "__main__": # import한 모듈 무시하고 main에 있는 것만 실행
    unittest.main(testRunner= HtmlTestRunner.HTMLTestRunner(output = '/Users/caseykim/Desktop/QA Stuffs/Selenium_Tutorial/Sample_Project/Greencart_test/Test_reports'))





