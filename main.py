import random
import re
import time

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

PAGE_URL = "https://www.skelbiu.lt/"

driver = webdriver.Chrome()
driver.maximize_window()
# time.sleep(5)
driver.implicitly_wait(5)

random_num = str(random.randint(1, 100))

# driver.get("https://elenta.lt/")
# cookie_btn = driver.find_element(By.XPATH, '/html/body/div[3]/div[2]/div[1]/div[2]/div[2]/button[1]')
# cookie_btn.click()

# ----------------------------REGISTRACIJA--------------------------------------------
# login_link = driver.find_element(By.XPATH, '//*[@id="header-container-nav"]/a[3]')
# login_link.click()
# register_link = driver.find_element(By.XPATH, '//*[@id="form"]/fieldset/table/tbody/tr[10]/td/p/a')
# register_link.click()
# input_user_name = driver.find_element(By.ID, 'UserName')
# input_user_name.send_keys('Marytė' + str(random_num))
# input_email = driver.find_element(By.ID, 'Email')
# input_email.send_keys('maryte_test' + random_num + '@exmaple.com')
# input_password = driver.find_element(By.ID, 'Password')
# input_password.send_keys('Testukas7*')
# input_password2 = driver.find_element(By.ID, 'Password2')
# input_password2.send_keys('Testukas7*')
# time.sleep(2)
# register_btn = driver.find_element(By.CLASS_NAME, 'bigNavBtn2')
# register_btn.click()

# -----------------------------SKELBIMAS--------------------------------------------------------------------------------
# add_ad_btn = driver.find_element(By.ID, 'submit-new-ad-nav-button')
# add_ad_btn.click()
# category_link = driver.find_element(By.XPATH, '//*[@id="select-top-category-list"]/li[2]/a')
# category_link.click()
# sub_category_link = driver.find_element(By.XPATH, '//*[@id="select-sub-category-list"]/li[2]/a')
# sub_category_link.click()
# input_title = driver.find_element(By.ID, 'title')
# input_title.send_keys('Ieškau namuko')
# input_desc = driver.find_element(By.ID, 'text')
# input_desc.send_keys('Ieškau mažiuko namuko ant jūros kranto')
# input_price = driver.find_element(By.ID, 'price')
# input_price.send_keys('2000')
# input_phone_num = driver.find_element(By.ID, 'phone')
# input_phone_num.send_keys('+37069999999')
# time.sleep(1)
# submit_btn = driver.find_element(By.ID, 'submit-button')
# submit_btn.click()
#
# file_input = driver.find_element(By.ID, "inputfile")
# file_input.send_keys(r'C:\Users\rasal\OneDrive\Desktop\namukas.jpeg')
# time.sleep(1)
# forward_btn = driver.find_element(By.ID, 'forward-button')
# forward_btn.click()
# forward_btn = driver.find_element(By.ID, 'forward-button')
# forward_btn.click()
#
# select = Select(driver.find_element(By.ID, 'StarsCount'))
# select.select_by_index(3)
#
# select = Select(driver.find_element(By.ID, 'StarsDaysCount'))
# select.select_by_index(5)
#
# submit_btn = driver.find_element(By.ID, 'submit')
# submit_btn.click()
#
# time.sleep(3)
# driver.quit()


# ============================== kategorijų nuorodų nurinkimas į sarašą ======================
#
# cage_blocks = main_container.find_elements(By.CLASS_NAME,'categBlock')
# hrefs = []
# for cb in cage_blocks:
#     for a in cb.find_elements(By.TAG_NAME, 'a'):
#         hrefs.append(a.get_attribute("href"))
# print(hrefs)
# ============================== kategorijų nuorodų nurinkimas į sarašą ======================

# ===============================SKELBIU.LT====================================================
driver.get(PAGE_URL)


def find_hrefs():
    driver.implicitly_wait(0)
    main_container = driver.find_element(By.ID, 'items-list-container')
    hrefs_container = main_container.find_element(By.CLASS_NAME, 'standard-list-container')
    hrefs = []
    for a in hrefs_container.find_elements(By.TAG_NAME, 'a'):
        href = a.get_attribute('href')

        aruodas_element = None
        try:
            aruodas_element = a.find_element(By.CLASS_NAME, "aruodas")
        except NoSuchElementException:
            pass

        # if not (href.startswith('https://www.kainos.lt') or href.startswith('https://autoplius.lt') or aruodas_element):
        if not href.startswith('https://www.kainos.lt'):
            hrefs.append(href)
    driver.implicitly_wait(5)
    return hrefs


def find_next_search_link():
    pagination_block = driver.find_element(By.XPATH, '//*[@id="pagination"]')
    for a in pagination_block.find_elements(By.TAG_NAME, 'a'):
        rel = a.get_attribute('rel')
        if rel == 'next':
            return a
    return None


def accept_cookies():
    cookie_btn = driver.find_element(By.ID, 'onetrust-accept-btn-handler')
    cookie_btn.click()


def search_by_keyword(keyword):
    search_input = driver.find_element(By.ID, 'searchKeyword')
    search_input.send_keys(keyword)
    search_button = driver.find_element(By.ID, 'searchButton')
    search_button.click()


# def print_hrefs_and_total():
#     search_total = driver.find_element(By.XPATH, '//*[@id="body-container"]/div[2]/div[1]/ul/li/span').text.strip(
#         '()').replace(" ", "")
#     if int(search_total) == 0:
#         print(f"Ups, jokių skelbimų nerasta...")
#     else:
#         hrefs = find_hrefs()
#         while True:
#             next_href = find_next_search_link()
#             if next_href:
#                 next_href.click()
#                 hrefs += find_hrefs()
#             else:
#                 break
#         # print(*hrefs, sep='\n')
#         print(f"Iš viso rado skelbiu.lt: {search_total} Iš viso yra iš tikrųjų: {len(hrefs)}. ")

def get_next_page_url(current_url):
    page_url_groups = re.match(r'^(https://www.skelbiu.lt/skelbimai/)(\d*)(\?.+)$', current_url)
    if page_url_groups:
        base_url, pg_num, ending = page_url_groups.groups()
        # print(base_url, pg_num, ending)
        if not pg_num:
            pg_num = 1
        next_page = int(pg_num) + 1
        return f"{base_url}{next_page}{ending}"
    else:
        raise ValueError(f"Unexpected URL format: {current_url}")


def print_hrefs_and_total():
    current_url = driver.current_url
    search_total = (driver.find_element(By.XPATH, '//*[@id="body-container"]/div[2]/div[1]/ul/li/span')
                    .text
                    .strip('()')
                    .replace(" ", ""))

    if int(search_total) == 0:
        print(f"Ups, jokių skelbimų nerasta...")
        return

    hrefs = []
    while True:
        hrefs += find_hrefs()
        pattern = r"/skelbimai/(\d*)"
        current_pg_match = re.search(pattern, current_url)
        current_pg_num = current_pg_match.group(1)
        if current_pg_num == '200':
            break
        next_page_url = get_next_page_url(current_url)
        driver.get(next_page_url)
        new_url = driver.current_url
        new_pg_match = re.search(pattern, new_url)
        new_pg_num = new_pg_match.group(1)
        if new_pg_num == '1':
            break
        current_url = new_url

    # print(*hrefs, sep='\n')
    print(f"Iš viso rado skelbiu.lt: {search_total}. Iš viso iš tikrųjų: {len(hrefs)}.")


accept_cookies()
search_by_keyword('namukas')  # telefonas 7372 arba 4800 arba 4766 / 4739
time.sleep(2)  # driver.implicitly_wait() - NEVEIKIA
print_hrefs_and_total()

time.sleep(1000)
