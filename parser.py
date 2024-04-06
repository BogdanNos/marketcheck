from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import json
from random import randint

service = Service(executable_path='./yandexdriver.exe')
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument("--window-size=1920,1080")
driver = webdriver.Chrome(service=service, options=options)

marketplaces = {}

driver.get("https://megamarket.ru/")
driver.execute_script("window.open('');") 
marketplaces["megamarket"] = driver.current_window_handle
driver.switch_to.window(driver.window_handles[1]) 

driver.get("https://www.wildberries.ru/")
driver.execute_script("window.open('');") 
marketplaces["wildberries"] = driver.current_window_handle
driver.switch_to.window(driver.window_handles[2]) 

driver.get("https://www.ozon.ru/")
driver.execute_script("window.open('');") 
marketplaces["ozon"] = driver.current_window_handle
driver.switch_to.window(driver.window_handles[3]) 

driver.get("https://market.yandex.ru/")
marketplaces["yandexmarket"] = driver.current_window_handle

def get_items_megamarket(product_name, sort = "popular"):
    sorting = 0
    if sort == "price":
        sorting = 1
    hash = randint(0,9999999999999)
    driver.execute_script(r'''fetch("https://megamarket.ru/api/mobile/v1/catalogService/catalog/search", {
    "headers": {
        "accept": "application/json",
        "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "content-type": "application/json",
        "sec-ch-ua": "\"Google Chrome\";v=\"123\", \"Not:A-Brand\";v=\"8\", \"Chromium\";v=\"123\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "x-requested-with": "XMLHttpRequest"
    },
    "referrer": "https://megamarket.ru/catalog/?q={search_name}&sort={sorting}",
    "referrerPolicy": "strict-origin-when-cross-origin",
    "body": "{\"requestVersion\":10,\"limit\":44,\"offset\":0,\"isMultiCategorySearch\":false,\"searchByOriginalQuery\":false,\"selectedSuggestParams\":[],\"expandedFiltersIds\":[],\"sorting\":{sorting},\"ageMore18\":null,\"addressId\":\"2gis_1267273050364753\",\"showNotAvailable\":true,\"selectedFilters\":[],\"searchText\":\"{search_name}\",\"auth\":{\"locationId\":\"66\",\"appPlatform\":\"WEB\",\"appVersion\":0,\"experiments\":{\"8\":\"2\",\"55\":\"2\",\"58\":\"2\",\"62\":\"1\",\"68\":\"2\",\"69\":\"1\",\"79\":\"3\",\"84\":\"2\",\"96\":\"2\",\"98\":\"1\",\"99\":\"1\",\"107\":\"2\",\"109\":\"2\",\"119\":\"1\",\"120\":\"2\",\"121\":\"2\",\"122\":\"2\",\"128\":\"1\",\"130\":\"1\",\"132\":\"2\",\"144\":\"3\",\"147\":\"3\",\"154\":\"1\",\"163\":\"2\",\"173\":\"1\",\"178\":\"1\",\"184\":\"3\",\"186\":\"1\",\"190\":\"1\",\"192\":\"2\",\"200\":\"2\",\"205\":\"2\",\"209\":\"1\",\"213\":\"1\",\"218\":\"1\",\"228\":\"2\",\"229\":\"2\",\"235\":\"2\",\"237\":\"2\",\"238\":\"2\",\"243\":\"1\",\"255\":\"2\",\"644\":\"1\",\"645\":\"2\",\"723\":\"2\",\"5779\":\"2\",\"20121\":\"2\",\"70070\":\"1\",\"85160\":\"2\"},\"os\":\"UNKNOWN_OS\"}}",
    "method": "POST",
    "mode": "cors",
    "credentials": "include"
    }).then((response) => response.text()).then((text) => {
            localStorage.setItem("megamarket_result_{hash}", text);
        });'''.replace(r"{hash}", str(hash)).replace(r"{search_name}", str(product_name)).replace(r"{sorting}", str(sorting)))
    storage = driver.execute_script("return window.localStorage;")
    while f"megamarket_result_{hash}" not in storage:
        storage = driver.execute_script("return window.localStorage;")
    items = storage[f"megamarket_result_{hash}"]
    items = json.loads(items)
    return items

def handle_megamarket(product_name, sorting):
    #привод к общему виду
    items = get_items_megamarket(product_name, sorting)
    if "error" in items:
        print("Error")
        return -1
    if "items" not in items:
        return -1
    items = items["items"]
    itemsRuled = []
    g = 0
    if len(items) != 0:
        while len(itemsRuled) != 5:
            item = items[g]
            if item["finalPrice"] != 0:
                itemsRuled.append({"name":item["goods"]["title"], "price": item["finalPrice"], "image": item["goods"]["images"][0], "url":item["goods"]["webUrl"]})
            
            g += 1
            if g >= len(items) - 1:
                break
    return  {"name" : "megamarket", "items" : itemsRuled, "sorting" : sorting}

def handle_wildberries(product_name):
    #привод к общему виду
    pass

def handle_request(product_name, sorting = "popular"):
    for name in marketplaces:
        driver.switch_to.window(marketplaces[name])
        if name == "megamarket":
            return [handle_megamarket(product_name, sorting)]
        elif name == "wildberries":
            handle_wildberries(product_name, sorting)
    return "handled"