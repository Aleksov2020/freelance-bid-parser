import time
import configparser
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

parse_links_list = ['https://www.weblancer.net/jobs/?page=1', 'https://www.weblancer.net/jobs/?page=2',
                    'https://www.weblancer.net/jobs/?page=3', 'https://www.weblancer.net/jobs/?page=3']

parse_links_list1 = ['https://freelance.ru/project/search/pro?c=&c%5B%5D=116&c%5B%5D=4&q=&m=or&e=&f=&t=&o=0&o=1',
                     'https://freelance.ru/project/search/pro?c%5B0%5D=116&c%5B1%5D=4&q=&m=or&e=&f=&t=&o=1&page=2&per-page=25',
                     'https://freelance.ru/project/search/pro?c%5B0%5D=116&c%5B1%5D=4&q=&m=or&e=&f=&t=&o=1&page=3&per-page=25',
                     'https://freelance.ru/project/search/pro?c%5B0%5D=116&c%5B1%5D=4&q=&m=or&e=&f=&t=&o=1&page=4&per-page=25']

TEMPLATE_GENERATOR = "Ваше шаблонное сообщение для поиска заказов"


def configure_browser():
    # start webdriver
    # load options for webdriver
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x935')
    return webdriver.Chrome(chrome_options=options)


def account_login(browser, wait):
    config = configparser.ConfigParser()
    config.read('configuration.ini')

    # login into weblancer.net
    browser.find_element(By.XPATH, '//a[contains(text(),"Вход")]').click()
    time.sleep(1)
    browser.find_element(By.NAME, "login").send_keys(config['account']['username'])
    browser.find_element(By.NAME, "password").send_keys(config['account']['password'])

    browser.find_element(By.XPATH, '//button[contains(text(),"Войти в аккаунт")]').click()

    time.sleep(.1)


def take_orders(browser):
    count = 0
    result_dict = {
        "title": [],
        "link": [],
        "time_ago": [],
        "category": []
    }

    browser.refresh()
    order_list = browser.find_elements(By.CLASS_NAME, "row.click_container-link.set_href")

    for order in order_list:
        count += 1

        title_html = order.find_element(By.CLASS_NAME, "click_target")
        title = title_html.text

        pinned = len(order.find_elements(By.XPATH, '//span[@class="icon-flag fixed_icon"]'))

        link = title_html.get_attribute('href')
        time_ago = order.find_element(By.CLASS_NAME, "tooltip").get_attribute("data-bs-original-title")
        category_l = order.find_element(By.CLASS_NAME, "col-sm-8.text-muted.dot_divided.text_field.d-sm-flex")
        category_list = category_l.find_elements(By.CLASS_NAME, "text-muted")
        category = ""
        for cat in category_list:
            category += cat.text + " "

        if count > pinned:
            result_dict["title"].append(title)
            result_dict["link"].append(link)
            result_dict["time_ago"].append(time_ago)
            result_dict["category"].append(category)

    return result_dict


def run_bot():
    rez_dict = {
        "title": [],
        "link": [],
        "time_ago": [],
        "category": []
    }

    # open order pages 1-4 on weblancer.net
    for link in parse_links_list:
        browser = configure_browser()
        wait = WebDriverWait(browser, 15)

        browser.get(link)

        # take all orders for current page
        temp_rez_dict = take_orders(browser)

        # add new orders to rezult dictionary
        rez_dict["title"] += temp_rez_dict["title"]
        rez_dict["link"] += temp_rez_dict["link"]
        rez_dict["time_ago"] += temp_rez_dict["time_ago"]
        rez_dict["category"] += temp_rez_dict["category"]

        # becouse we only want to see 10-20 orders in the interface
        if len(rez_dict["title"]) >= 10:
            return rez_dict


def send_request(link, template=TEMPLATE_GENERATOR, price=100, time_need=5):
    browser = configure_browser()
    browser.get(link)
    wait = WebDriverWait(browser, 15)
    account_login(browser, wait)

    browser.refresh()
    try:
        browser.find_element(By.ID, 'bid_amount').send_keys(price)
        browser.find_element(By.ID, 'bid_days').send_keys(time_need)

        browser.find_element(By.NAME, 'comment').send_keys(template)
        browser.find_element(By.ID, 'place_bid_btn').click()
    except:
        print('Error with this bid')

    browser.quit()


def open_order(link, template=TEMPLATE_GENERATOR, price=100, time_need=5):
    options = webdriver.ChromeOptions()
    options.add_argument('window-size=1920x935')
    browser = webdriver.Chrome(chrome_options=options)
    browser.get(link)

    wait = WebDriverWait(browser, 15)
    account_login(browser. wait)

    time.sleep(.1)
    browser.refresh()
    try:
        browser.find_element(By.ID, 'bid_amount').send_keys(price)
        browser.find_element(By.ID, 'bid_days').send_keys(time_need)

        browser.find_element(By.NAME, 'comment').send_keys(template)
    except:
        pass


def run_bot2():
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x935')
    driver = webdriver.Chrome(chrome_options=options)
    driver.get("https://freelance.ru/login/")
    time.sleep(2)
    # login
    field1 = driver.find_element_by_id("login")
    field1.send_keys("aleksov2020@gmail.com")
    field2 = driver.find_element_by_id("passwd")
    field2.send_keys("m10342m10342")
    time.sleep(2)
    try:
        driver.find_element(By.XPATH, ".//input[@value = 'Вход']").click()
    except:
        try:
            driver.find_element(By.XPATH, ".//input[@value = 'Log In']").click()
        except:
            pass
    time.sleep(.1)
    count = 0
    order_list = []
    result_dict = {
        "title": [],
        "link": [],
        "time_ago": [],
        "category": []
    }
    for link in parse_links_list1:
        driver.get(link)
        time.sleep(.1)
        count = len(order_list)
        order_list1 = driver.find_elements_by_class_name("box-shadow.project")
        for i in range(len(order_list1)):
            try:
                order_list1[i].find_element_by_class_name("for-business.text-success")
            except:
                if len(order_list) < 20:
                    order_list.append(order_list1[i])
                else:
                    pass
        new_list_order = []
        for i in range(count, len(order_list)):
            new_list_order.append(order_list[i])
        for order in new_list_order:
            title_html = order.find_element_by_class_name("title")
            title = title_html.text
            result_dict["title"].append(title)
            link = title_html.find_element_by_tag_name("a").get_attribute('href')
            result_dict["link"].append(link)
            time_ago = order.find_element_by_class_name("timeago").get_attribute('title')
            result_dict["time_ago"].append(time_ago)
            category_l = order.find_element_by_class_name("specs-list")
            category_list = category_l.find_elements_by_tag_name("span")
            category = ""
            for cat in category_list:
                category += cat.text + " "
            result_dict["category"].append(category)
    return result_dict
