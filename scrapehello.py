# ### get data from saved html files, 200 items with value dwjz1/2 ljjz1/2 rzzz rzzl
# from bs4 import BeautifulSoup

BASE_URL = 'http://fund.eastmoney.com/'
FUNDS_PATH1 = 'fund.html#os_0;isall_0;ft_;pt_1'
FUNDS_PATH2 = 'cnjy_jzzzl.html'
CACHE_FILE_NAME1 = 'cacheFunds1.json'
CACHE_FILE_NAME2 = 'cacheFunds2.json'
CACHE_DICT = {}
FUNDS = {}

import json
import time
from bs4 import BeautifulSoup
import requests

def load_cache(filename):
    try:
        cache_file = open(filename, 'r')
        cache_file_contents = cache_file.read()
        cache = json.loads(cache_file_contents)
        cache_file.close()
    except:
        cache = {}
    return cache

def save_cache(cache, filename):
    cache_file = open(filename, 'w')
    contents_to_write = json.dumps(cache)
    cache_file.write(contents_to_write)
    cache_file.close()

def make_url_request_using_cache(url, cache, filename):
    if(url in cache.keys()):
        print('Using cache')
        return cache[url]
    print('Fetching data...')
    time.sleep(1)
    response = requests.get(url)
    cache[url] = response.text
    save_cache(cache, filename)
    return cache[url]

class Funds:
    def __init__(self, jzgs, dwjz, ljjz, lspng, lsjz, zzl):
        self.jzgs = jzgs
        self.dwjz = dwjz
        self.ljjz = ljjz
        self.zzl = zzl
        self.lspng = lspng
        self.lsjz = lsjz


def data_collection(response):

    soup = BeautifulSoup(response.text, 'html.parser')

    ##################### Page 2 #########################
    funds_cache = {}
    currentPage_details_path = soup.find_all('td', class_='tol')
    for path in currentPage_details_path[:10]:
        name = path.find('a')['href'][:-5]
        funds_cache[name] = {}
        currentPage_details_url = BASE_URL + name + '.html'
        response = requests.get(currentPage_details_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        details = soup.find_all('div',class_='fundInfoItem')[0].contents

        dataOfFund = details[1]
        jzgs = dataOfFund.find(class_='dataItem01').contents[1].text
        temp = dataOfFund.find(class_='dataItem02').contents
        dwjz = temp[1].contents[0].text
        zzl = temp[1].contents[1].text
        ljjz = dataOfFund.find(class_='dataItem03').contents[1].text


        ##################### Page 3 #########################
        history_url = temp[0].find('a')['href']
        response = requests.get(history_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        lspng = soup.find('div', class_='listcomm jz_list').find('img')
        lsjz = soup.find('table', class_='w782 comm lsjz')       # ajax异步获取数据，待解决


        ########## caching ###########
        funds_cache[name] = Funds(jzgs, dwjz, ljjz, lspng, lsjz, zzl)
        # {'jzgs': jzgs, 'dwjz': dwjz, 'ljjz': ljjz, 'lspng': lspng, 'lsjz': lsjz, 'zzl': zzl}

    return funds_cache


CACHE_DICT = load_cache(CACHE_FILE_NAME1)
url = BASE_URL + FUNDS_PATH1
url_text = make_url_request_using_cache(url, CACHE_DICT, CACHE_FILE_NAME1)
response = requests.get(url)
# response = url_text
FUNDS['OE'] = data_collection(response)

CACHE_DICT = load_cache(CACHE_FILE_NAME2)
url = BASE_URL + FUNDS_PATH2
url_text = make_url_request_using_cache(url, CACHE_DICT, CACHE_FILE_NAME2)
response = requests.get(url)
# response = url_text
FUNDS['ET'] = data_collection(response)

print(FUNDS)

