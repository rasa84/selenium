import random
import unittest

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select


class AdTest(unittest.TestCase):
    EXPECTED = "Eiti į elektroninę bankininkystę"

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.implicitly_wait(5)
        self.driver.get("https://elenta.lt/registracija")
        self.driver.find_element(By.XPATH, '/html/body/div[3]/div[2]/div[2]/div[2]/div[2]/button[1]').click()
        self.random_num = str(random.randint(1, 1000))
        self.driver.find_element(By.ID, 'submit-new-ad-nav-button').click()
        self.driver.find_element(By.XPATH, '//*[@id="select-top-category-list"]/li[2]/a').click()
        self.driver.find_element(By.XPATH, '//*[@id="select-sub-category-list"]/li[2]/a').click()

    def tearDown(self):
        self.driver.quit()

    def test_upload_add_successfully(self):
        self.fill_in_main_info('Ieškau namuko', 'Ieškau mažiuko namuko ant jūros kranto', '+37069999999', '2000')
        actual = self.upload_add()

        self.assertEqual(AdTest.EXPECTED, actual)

    def test_upload_add_fails_with_incorrect_phone_number(self):
        expected_err_message = 'Blogas tel. numeris'

        self.fill_in_main_info('Ieškau namuko', 'Ieškau mažiuko namuko ant jūros kranto', '69999999', '2000')

        err_msg_field = self.driver.find_element(By.ID, 'pe')

        self.assertEqual(expected_err_message, err_msg_field.text)

    def fill_in_main_info(self, title, description, phone, price):
        input_title = self.driver.find_element(By.ID, 'title')
        input_title.send_keys(title)
        input_desc = self.driver.find_element(By.ID, 'text')
        input_desc.send_keys(description)
        input_price = self.driver.find_element(By.ID, 'price')
        input_price.send_keys(price)
        input_phone_num = self.driver.find_element(By.ID, 'phone')
        input_phone_num.send_keys(phone)
        submit_btn = self.driver.find_element(By.ID, 'submit-button')
        submit_btn.click()

    def upload_add(self):
        # file_input = self.driver.find_element(By.ID, "inputfile")
        # file_input.send_keys(r'C:\Users\rasal\OneDrive\Desktop\namukas.jpeg')
        forward_btn = self.driver.find_element(By.ID, 'forward-button')
        forward_btn.click()
        forward_btn = self.driver.find_element(By.ID, 'forward-button')
        forward_btn.click()
        select = Select(self.driver.find_element(By.ID, 'StarsCount'))
        select.select_by_index(3)
        select = Select(self.driver.find_element(By.ID, 'StarsDaysCount'))
        select.select_by_index(5)
        submit_btn = self.driver.find_element(By.ID, 'submit')
        submit_btn.click()
        try:
            return self.driver.find_element(By.XPATH, '//*[@id="payment-system-ebanking-list"]/li[2]/a').text
        except NoSuchElementException:
            return ''
