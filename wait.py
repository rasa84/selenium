from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

driver = webdriver.Chrome()
driver.maximize_window()
driver.implicitly_wait(5)


def accept_cookies():
    cookie_btn = driver.find_element(By.ID, 'CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll')
    cookie_btn.click()


def approve_age():
    age_btn = driver.find_element(By.XPATH,
                                  '//*[@id="app__inner"]/div[2]/div/div/div/div/div[2]/div[3]/div/div[1]/button')
    age_btn.click()


def search():
    driver.get("https://vynoteka.lt/")
    accept_cookies()
    approve_age()
    WebDriverWait(driver, 25).until(
        EC.element_to_be_clickable((By.ID, "omnisend-form-63ff1f31b40d6530aba59a6d-close-action"))).click()
    input_search = driver.find_element(By.XPATH,
                                       '//*[@id="app__header"]/div[2]/div/div/div[3]/div/div/div/form/div[1]/div/input')
    input_search.send_keys('carmenere')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "products-table__body")))
    driver.find_element(By.XPATH, '//*[@id="app__header"]/div[2]/div/div/div[3]/div/div/div/form/div[1]/button').click()


search()
