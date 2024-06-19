from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from lxml import etree 
import urllib.request, urllib.error 

#from seleniumwire import webdriver
import os
import zipfile
from time import sleep
import json
from random import randint

proxy_username = 'yR6eA1'
proxy_password = 'yRQaK0'
ip = "212.81.38.37"
port = "9879"

seleniumwire_options = {
    'proxy': {
        'http': f'http://{proxy_username}:{proxy_password}@{ip}:{port}'
    }
}

service = Service(executable_path='./chromedriver.exe')
options = webdriver.ChromeOptions()

#options.add_argument(f"--proxy-server={proxy}")
options.add_argument('--ignore-certificate-errors')
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument("--window-size=1920,1080")
#options.add_argument('headless')


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

from threading import Thread
import functools

def timeout(seconds_before_timeout):
    def deco(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            res = [Exception('function [%s] timeout [%s seconds] exceeded!' % (func.__name__, seconds_before_timeout))]
            def newFunc():
                try:
                    res[0] = func(*args, **kwargs)
                except Exception as e:
                    res[0] = e
            t = Thread(target=newFunc)
            t.daemon = True
            try:
                t.start()
                t.join(seconds_before_timeout)
            except Exception as e:
                print(e)
                print('error starting thread')
                raise e
            ret = res[0]
            if isinstance(ret, BaseException):
                raise ret
            return ret
        return wrapper
    return deco

def get_items_ozon(product_name, sort = "popular"):
    sorting = "score"
    if sort == "price":
        sorting = "price"
    hash = randint(0,9999999999999)
    url = f"https://www.ozon.ru/search/?text={str(product_name)}&from_global=true&sorting={str(sorting)}"
    driver.execute_script(r'''fetch("https://www.ozon.ru/search/?text={search_name}&from_global=true&sorting={sorting}", {
    "headers": {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "ru,en;q=0.9,pt;q=0.8",
        "sec-ch-ua": "\"Not_A Brand\";v=\"8\", \"Chromium\";v=\"120\", \"YaBrowser\";v=\"24.1\", \"Yowser\";v=\"2.5\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "service-worker-navigation-preload": "true",
        "upgrade-insecure-requests": "1"
    },
    "referrer": "https://www.ozon.ru/",
    "referrerPolicy": "no-referrer-when-downgrade",
    "body": null,
    "method": "GET",
    "mode": "cors",
    "credentials": "include"
    }).then((response) => response.text()).then((text) => {
            localStorage.setItem("ozon_result_{hash}", text);
        });'''.replace(r"{hash}", str(hash)).replace(r"{search_name}", str(product_name)).replace(r"{sorting}", str(sorting)))
    storage = driver.execute_script("return window.localStorage;")
    while f"ozon_result_{hash}" not in storage:
        storage = driver.execute_script("return window.localStorage;")
    response = storage[f"ozon_result_{hash}"]

    hash = randint(0,9999999999999)
    if "location.replace" in response:
        url = response.split('location.replace("')[1].split('");</script>')[0].replace('\\',"")
        driver.execute_script(r'''fetch("{url}", {
        "headers": {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-language": "ru,en;q=0.9,pt;q=0.8",
            "sec-ch-ua": "\"Not_A Brand\";v=\"8\", \"Chromium\";v=\"120\", \"YaBrowser\";v=\"24.1\", \"Yowser\";v=\"2.5\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "service-worker-navigation-preload": "true",
            "upgrade-insecure-requests": "1"
        },
        "referrer": "https://www.ozon.ru/",
        "referrerPolicy": "no-referrer-when-downgrade",
        "body": null,
        "method": "GET",
        "mode": "cors",
        "credentials": "include"
        }).then((response) => response.text()).then((text) => {
                localStorage.setItem("ozon_result_{hash}", text);
            });'''.replace(r"{hash}", str(hash)).replace(r"{url}", str(url)))
        
        storage = driver.execute_script("return window.localStorage;")
        while f"ozon_result_{hash}" not in storage:
            storage = driver.execute_script("return window.localStorage;")
        response = storage[f"ozon_result_{hash}"]
    return response, url
@timeout(5)
def handle_ozon(product_name, sorting):
    #привод к общему виду
    itemsRuled = []
    response, url = get_items_ozon(product_name, sorting)
    
    
    itemsRuled = request_ozon(response, "//div[@id='paginatorContent'][1]/div/div/div",
                              ".//div/a/div/span",
                              "//div[@id='paginatorContent'][1]/div/div/div/div/div/div/span[1]",
                              ".//a/div/div/div/img",
                              ".//div/a", True)
    if itemsRuled == []:
        itemsRuled = request_ozon(response, "//div[@id='paginatorContent'][1]/div/div/div/div",
                                ".//div/a/div/span",
                                "//div[@id='paginatorContent'][1]/div/div/div/div/div/div/div/span[1]",
                                ".//a/div/div/img",
                                ".//div/a", False)
    return  {"name" : "ozon", "items" : itemsRuled, "sorting" : sorting, "search_url": url}

def request_ozon(response, path_items, path_name, path_price, path_image, path_url, category):
    def selector_no_cat(g):
        return (g+1)*4-1
    itemsRuled = []
    soup = BeautifulSoup(response,"lxml")
    dom = etree.HTML(str(soup))
    items = dom.xpath(path_items)
    g = 0
    if len(items) != 0:
        while len(itemsRuled) != 3:
            item = items[g]
            try:
                name = item.xpath(path_name)[0].text
                price = int(dom.xpath(path_price)[selector_no_cat(g) if category else g].text.replace(" ","").replace("₽",""))
                image = item.xpath(path_image)[0].attrib['src']
                url = "https://www.ozon.ru" + item.xpath(path_url)[0].attrib['href']
                itemsRuled.append({"name": name, "price": price, "image": image, "url": url})
                g += 1
            except: 
                break
            if g >= len(items) - 1:
                break
    return  itemsRuled

def get_items_megamarket(product_name, sort="popular"):
    sorting = 0
    if sort == "price":
        sorting = 1
    hash = randint(0, 9999999999999)
    url = f"https://megamarket.ru/catalog/?q={product_name}#?sort={sorting}"
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
    return url, items
@timeout(5)
def handle_megamarket(product_name, sorting):
    # привод к общему виду
    itemsRuled = []
    url, items = get_items_megamarket(product_name, sorting)
    if "error" in items:
        print("Error")
        return {"name": "megamarket", "items": itemsRuled, "sorting": sorting}
    if "items" not in items:
        return {"name": "megamarket", "items": itemsRuled, "sorting": sorting}
    items = items["items"]
   
    g = 0
    if len(items) != 0:
        while len(itemsRuled) != 3:
            item = items[g]
            if item["finalPrice"] != 0:
                itemsRuled.append({"name": item["goods"]["title"], "price": item["finalPrice"],
                                  "image": item["goods"]["images"][0], "url": item["goods"]["webUrl"]})
            g += 1
            if g >= len(items) - 1:
                break
    return {"name": "megamarket", "items": itemsRuled, "sorting": sorting, "search_url": url}

def get_items_yandex(product_name, sort="popular"):
    if sort == "popular":
        url = f"https://market.yandex.ru/search?text={product_name}"
    else:
        url = f"https://market.yandex.ru/search?text={product_name}&how=aprice"
    driver.get(url)
    try:
        catalog = WebDriverWait(driver, 2).until(EC.presence_of_element_located(
            (By.XPATH, "//div[@data-zone-name='searchResults']")))
        items = catalog.find_elements(
            By.XPATH, './/div[@data-apiary-widget-name="@light/Organic"]')
        return url, items
    except Exception as e:
        print(e)
        return url, []

@timeout(5)    
def handle_yandex(product_name, sorting):
    # привод к общему виду
    url, items = get_items_yandex(product_name, sorting)
    itemsRuled = []
    g = 0
    if len(items) != 0:
        while len(itemsRuled) != 3:
            item = items[g]
            href = item.find_element(
                By.XPATH, ".//a[@data-auto='snippet-link']").get_attribute("href")
            title = item.find_element(
                By.XPATH, './/h3[@data-auto="snippet-title"]').text
            price = item.find_element(
                By.XPATH, './/span[@data-auto="snippet-price-current"]').text
            image = item.find_element(
                By.XPATH, ".//div[@data-zone-name='picture']/img").get_attribute("src")
            itemsRuled.append({"name": title, "price": int(price.replace(" ","").replace("₽","")),
                              "image": image, "url": href})
            g += 1
            if g >= len(items) - 1:
                break
    return {"name": "yandex", "items": itemsRuled, "sorting": sorting, "search_url": url}

def get_items_wildberries(product_name, sort = "popular"):
    sorting = 'popular'
    if sort == "price":
        sorting = 'priceup'
    hash = randint(0,9999999999999)
    url = f"https://www.wildberries.ru/catalog/0/search.aspx?page=1&sort={sorting}&search={product_name}"
    driver.execute_script(r'''fetch("https://search.wb.ru/exactmatch/ru/male/v5/search?ab_testing=false&appType=1&curr=rub&dest=-5818883&query={search_name}&resultset=catalog&sort={sorting}&spp=30&suppressSpellcheck=false&uclusters=2&uiv=2&uv=qtsmiaYeHdCuX6jQLkgsVKgPMHqlxaJjqUKlw6eRrYwpVq6BqomxhiggshMlwayuLrCwM6zUpNspZqsvqhatoa12qEktNyqML0gyEZ0MrJwmw6zUqY0wTqdSsouNNqpGMeOolCtTIFKr0o3bJ4alGC8KLKckGafpqfSwpK38o3QqoitRNTwq8LAFshwvUai9Li-wmah7CMInAq0cKciq6CFdrkgsrSuerYynW6r1LHGriDCrsJinVjA_q5YjN6iDpT0tPqa2rwyt5KcnHfcqvTIlqlYoRSf3LCElEydfsgAuby-6K2uuGyKdLoAlqC7cLjkqNqgDJuudnalWMtOoJw", {
  "headers": {
    "accept": "*/*",
    "accept-language": "ru,en;q=0.9,pt;q=0.8",
    "authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE3MTI5MTIxMzQsInZlcnNpb24iOjIsInVzZXIiOiIyMDY3MTA3MSIsInNoYXJkX2tleSI6IjEwIiwiY2xpZW50X2lkIjoid2IiLCJzZXNzaW9uX2lkIjoiYTZlYTg5ODZhMjc3NDUxMDkxOTdhODU3N2I5MDJmNTIiLCJ1c2VyX3JlZ2lzdHJhdGlvbl9kdCI6MTY3NDIwNzA4MywidmFsaWRhdGlvbl9rZXkiOiI0NTRkOWE5NmE3MDU2ZGNmMzE1M2M4NmU0Y2Y5ZDkzZDE2ODcyZGI4YzZjN2I0MjViMzA2MzVhZjYzZWZiZDgyIiwicGhvbmUiOiJzbDI2ZVNOOUxoOHRIcmlqYXFHMlF3PT0ifQ.bgyLowYdvjmnnaA7EBKFpHnXYT4oVcC8I2A5q6Pj3e98lTgJXkoPNAgQfD49AkEm_wZJI9sb1FVBmjnD3hNeoUeKGUmT4xVj2BHLD-QEoZJtBMtptK0aZ6W9aqdJgznbsWG2tXee3GHuooxevPLKVCaa3Jo3kbc1Ak1Yl8UkfhyvyafHeyf6YATfQAp3nJ8kq5ZEF1vmuykoTUZQI2Cb3haMjpLTLVvajwO1dAJFmYgzbtYp3PrUcSJZ-0IvzAQcKDHVOy0kC9Ss66dI5RwIGSC7ipSvp0urQ-OA5sben32QY7StrGBQnELKbpO06GtQeT-QMtNWRbGQZHtEpKVRNw",
    "sec-ch-ua": "\"Not_A Brand\";v=\"8\", \"Chromium\";v=\"120\", \"YaBrowser\";v=\"24.1\", \"Yowser\";v=\"2.5\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "cross-site",
    "x-queryid": "qid307941734171006440720240412093420",
    "x-userid": "20671071"
  },
  "referrer": "https://www.wildberries.ru/catalog/0/search.aspx?page=1&sort={sorting}&search={search_name}",
  "referrerPolicy": "no-referrer-when-downgrade",                          
  "body": null,
  "method": "GET",
  "mode": "cors",
  "credentials": "include"
}).then((response) => response.text()).then((text) => {
            localStorage.setItem("wildberries_result_{hash}", text);
        });'''.replace(r"{hash}", str(hash)).replace(r"{search_name}", str(product_name)).replace(r"{sorting}", str(sorting)))
    storage = driver.execute_script("return window.localStorage;")
    while f"wildberries_result_{hash}" not in storage:
        storage = driver.execute_script("return window.localStorage;")
    items = storage[f"wildberries_result_{hash}"]
    items = json.loads(items)
    return url, items
@timeout(5)    
def handle_wildberries(product_name, sorting):
    def get_basket(id):
        vol = id // 100000
        basket = "01"
        if (vol >= 0 and vol <= 143): 
            basket = "01"
        elif (vol >= 144 and vol <= 287): 
            basket = "02"
        elif (vol >= 288 and vol <= 431): 
            basket = "03"
        elif (vol >= 432 and vol <= 719): 
            basket = "04"
        elif (vol >= 720 and vol <= 1007): 
            basket = "05"
        elif (vol >= 1008 and vol <= 1061): 
            basket = "06"
        elif (vol >= 1062 and vol <= 1115): 
            basket = "07"
        elif (vol >= 1116 and vol <= 1169): 
            basket = "08"
        elif (vol >= 1170 and vol <= 1313): 
            basket = "09"
        elif (vol >= 1314 and vol <= 1601): 
            basket = "10"
        elif (vol >= 1602 and vol <= 1655): 
            basket = "11"
        elif (vol >= 1656 and vol <= 1919): 
            basket = "12"
        elif (vol >= 1920 and vol <= 2045): 
            basket = "13"
        else:
            basket = "14"

        return basket
    
    #привод к общему виду
    url, items = get_items_wildberries(product_name, sorting)
    itemsRuled = []
    if "error" in items:
        print("Error")
        return  {"name" : "wildberries", "items" : itemsRuled, "sorting" : sorting}

    items = items["data"]["products"]
    g = 0
    if len(items) != 0:
        while len(itemsRuled) != 3:
            item = items[g]
            price = item["sizes"][0]["price"]["total"]
            idItem = str(item["id"])
            image = f'https://basket-{get_basket(item["id"])}.wbbasket.ru/vol{idItem[:-5]}/part{idItem[:-3]}/{idItem}/images/big/1.webp'
            try:
                conn = urllib.request.urlopen(image)
            except urllib.error.URLError as e:
                if e.code == 404:
                    image = "https://cdn-icons-png.flaticon.com/512/8437/8437807.png"

            itemsRuled.append({"name":item["name"], "price": int(str(price)[:-2]), "image": image, "url":f'https://www.wildberries.ru/catalog/{idItem}/detail.aspx'})
            g += 1
            if g >= len(items) - 1:
                break
    return  {"name" : "wildberries", "items" : itemsRuled, "sorting" : sorting, "search_url": url}


def searchBest(bigItem, sorting):
    pricemin = 9999999999
    marketplace = ''
    url = ''
    for items in bigItem:
        for item in items['items']:
            price = item['price']
            #print(price)
            if(price < pricemin):
                marketplace = items['name']
                url = items['search_url']
                pricemin = price
    return {sorting: {"marketplace": marketplace, "price": pricemin, "url":url}}

def handle_request(product_name):
    itemsPrice = []
    itemsPopular = []
    best = []
    for name in marketplaces:
        driver.switch_to.window(marketplaces[name])
        if name == "megamarket":
            try:
                itemsPrice.append(handle_megamarket(product_name, "price"))
            except:
                itemsPrice.append({"name" : "megamarket", "items" : [], "sorting" : "price"})
            try:
                itemsPopular.append(handle_megamarket(product_name, "popular"))
            except:
                itemsPopular.append({"name" : "megamarket", "items" : [], "sorting" : "popular"})
        elif name == "wildberries":
            try:
                itemsPrice.append(handle_wildberries(product_name, "price"))
            except:
                itemsPrice.append({"name" : "wildberries", "items" : [], "sorting" : "price"})
            try:
                itemsPopular.append(handle_wildberries(product_name, "popular"))
            except:
                itemsPopular.append({"name" : "wildberries", "items" : [], "sorting" : "popular"})
        elif name == "yandexmarket":
            try:
                itemsPrice.append(handle_yandex(product_name, "price"))
            except:
                itemsPrice.append({"name" : "yandex", "items" : [], "sorting" : "price"})
            try:
                itemsPopular.append(handle_yandex(product_name, "popular"))
            except:
                itemsPopular.append({"name" : "yandex", "items" : [], "sorting" : "popular"})
        elif name == "ozon":
            try:
                itemsPrice.append(handle_ozon(product_name, "price"))
            except:
                itemsPrice.append({"name" : "ozon", "items" : [], "sorting" : "price"})
            try:
                itemsPopular.append(handle_ozon(product_name, "popular"))
            except:
                itemsPopular.append({"name" : "ozon", "items" : [], "sorting" : "popular"})
    try:
        temp = searchBest(itemsPrice, 'price')
        temp.update(searchBest(itemsPopular, 'popular'))
    except:
        pass


    return {"popular": itemsPopular, "price": itemsPrice, "best": temp}

def refresh(marketplace):
    driver.switch_to.window(marketplaces[marketplace])
    driver.refresh()


'''
def get_items_ozon2(product_name, sort = "popular"):
    sorting = "score"
    if sort == "price":
        sorting = "price"
    url = "https://www.ozon.ru/search/?text={search_name}&from_global=true&sorting={sorting}".replace(r"{search_name}", str(product_name)).replace(r"{sorting}", str(sorting))
    driver.get(url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, "//form[@action='/search']"))).send_keys(product_name)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    
    try:
        items = WebDriverWait(driver, 5).until(EC.presence_of_element_located(
            (By.XPATH, "//div[@id='paginatorContent'][1]/div/div/div/div")))
        return items
    except:
        return []
@timeout(5)    
def handle_ozon2(product_name, sorting):
    #привод к общему виду
    items = get_items_ozon2(product_name, sorting)
    itemsRuled = []
    g = 0
    if len(items) != 0:
        while len(itemsRuled) != 3:
            item = items[g]
            href = item.find_element(
                By.XPATH, ".//a/div/div/img").get_attribute("href")
            title = item.find_element(
                By.XPATH, './/div/a/div/span').text
            price = item.find_element(
                By.XPATH, './/div/div/span').text
            image = item.find_element(
                By.XPATH, ".//a/div/div/img").get_attribute("src")
            itemsRuled.append({"name": title, "price": price,
                              "image": image, "url": href})
            g += 1
            if g >= len(items) - 1:
                break
    return {"name": "yandex", "items": itemsRuled, "sorting": sorting} '''
