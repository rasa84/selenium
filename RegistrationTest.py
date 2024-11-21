import random
import unittest

import unidecode
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from unidecode import unidecode


class RegistrationTest(unittest.TestCase):
    REGISTRATION_SUCCESSFUL_MESSAGE = "Jūs sėkmingai prisiregistravote!"

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.implicitly_wait(5)
        self.driver.get("https://elenta.lt/registracija")
        self.driver.find_element(By.XPATH, '/html/body/div[3]/div[2]/div[2]/div[2]/div[2]/button[1]').click()
        self.random_num = str(random.randint(1, 1000))
        self.driver.implicitly_wait(0)

    def tearDown(self):
        self.driver.quit()

    def test_register_successfully(self):
        result = self.register('Marytė', '@example.com', 'Testukas7*')

        self.assertIn(RegistrationTest.REGISTRATION_SUCCESSFUL_MESSAGE, result)

    def test_register_fails_with_existing_username(self):
        expected_err_message = 'Vartotojas tokiu vardu jau įregistruotas. Bandykite pasirinkti kitą.'

        self.register('Marytė', '@example111.com', 'Testukas7*', False)
        self.driver.implicitly_wait(5)
        self.driver.get("https://elenta.lt/registracija")
        self.driver.implicitly_wait(0)
        result = self.register('Marytė', '@example222.com', 'Testukas7*', False)
        err_msg_field = self.driver.find_element(By.XPATH,
                                                 '//*[@id="main-container"]/form/fieldset/table/tbody/tr[1]/td[2]/span')

        self.assertNotIn(RegistrationTest.REGISTRATION_SUCCESSFUL_MESSAGE, result)
        self.assertEqual(expected_err_message, err_msg_field.text)

    def test_register_fails_with_missing_username(self):
        expected_err_message = 'Įveskite vartotojo vardą.'

        result = self.register(user_name='',
                               email='test@example.com',
                               password='Testukas7*',
                               include_random_suffix=False)
        err_msg_field = self.driver.find_element(By.XPATH,
                                                 '//*[@id="main-container"]/form/fieldset/table/tbody/tr[1]/td[2]/span')

        self.assertNotIn(RegistrationTest.REGISTRATION_SUCCESSFUL_MESSAGE, result)
        self.assertEqual(expected_err_message, err_msg_field.text)

    def test_register_fails_with_missing_password(self):
        expected_err_message = 'Įveskite slaptažodį.'

        result = self.register('Marytė', '@example.com', '')
        err_msg_field = self.driver.find_element(By.XPATH,
                                                 '// *[ @ id = "main-container"] / form / fieldset / table / tbody / tr[7] / td[2] / span')

        self.assertNotIn(RegistrationTest.REGISTRATION_SUCCESSFUL_MESSAGE, result)
        self.assertEqual(expected_err_message, err_msg_field.text)

    def test_register_fails_with_short_password(self):
        expected_err_message = 'Įvestas slaptažodis per trumpas.'

        result = self.register('Marytė', '@example.com', 'abc')
        err_msg_field = self.driver.find_element(By.XPATH,
                                                 '// *[ @ id = "main-container"] / form / fieldset / table / tbody / tr[7] / td[2] / span')

        self.assertNotIn(RegistrationTest.REGISTRATION_SUCCESSFUL_MESSAGE, result)
        self.assertEqual(expected_err_message, err_msg_field.text)

    def test_register_fails_with_existing_email(self):
        expected_err_message = 'Toks el. pašto adresas jau įregistruotas.'

        self.register(user_name='Marytė888',
                      email='maryte888@example.com',
                      password='Testukas7*',
                      include_random_suffix=False)
        self.driver.implicitly_wait(5)
        self.driver.get("https://elenta.lt/registracija")
        self.driver.implicitly_wait(0)
        result = self.register(user_name='Petriukas888',
                               email='maryte888@example.com',
                               password='Testukas7*',
                               include_random_suffix=False)
        err_msg_field = self.driver.find_element(By.XPATH,
                                                 '//*[@id="main-container"]/form/fieldset/table/tbody/tr[4]/td[2]/span')

        self.assertNotIn(RegistrationTest.REGISTRATION_SUCCESSFUL_MESSAGE, result)
        self.assertEqual(expected_err_message, err_msg_field.text)

    def test_register_fails_with_invalid_email_format(self):
        expected_err_message = 'El. pašto adresas nėra tinkamas.'

        result = self.register('Marytė', 'example.com', 'Testukas7*')
        err_msg_field = self.driver.find_element(By.XPATH,
                                                 '//*[@id="main-container"]/form/fieldset/table/tbody/tr[4]/td[2]/span')

        self.assertNotIn(RegistrationTest.REGISTRATION_SUCCESSFUL_MESSAGE, result)
        self.assertEqual(expected_err_message, err_msg_field.text)

    def test_register_fails_with_special_characters_in_email(self):
        expected_err_message = 'El. pašto adresas nėra tinkamas.'

        result = self.register('Marytė', '@example^^.com', 'Testukas7*')
        err_msg_field = self.driver.find_element(By.XPATH,
                                                 '//*[@id="main-container"]/form/fieldset/table/tbody/tr[4]/td[2]/span')

        self.assertNotIn(RegistrationTest.REGISTRATION_SUCCESSFUL_MESSAGE, result)
        self.assertEqual(expected_err_message, err_msg_field.text)

    def register(self,
                 user_name='Marytė',
                 email_domain='',
                 password='Testukas7*',
                 include_random_suffix=True,
                 email=''):
        if include_random_suffix:
            user_name = user_name + str(self.random_num)
        if email_domain != '':
            email = unidecode(user_name.lower()) + email_domain
        input_user_name = self.driver.find_element(By.ID, 'UserName')
        input_user_name.send_keys(user_name)
        input_email = self.driver.find_element(By.ID, 'Email')
        input_email.send_keys(email)
        input_password = self.driver.find_element(By.ID, 'Password')
        input_password.send_keys(password)
        input_password2 = self.driver.find_element(By.ID, 'Password2')
        input_password2.send_keys(password)
        register_btn = self.driver.find_element(By.CLASS_NAME, 'bigNavBtn2')
        register_btn.click()
        try:
            return self.driver.find_element(By.CLASS_NAME, 'info').text
        except NoSuchElementException:
            return ''
