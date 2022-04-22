# ### get data from saved html files, 200 items with value dwjz1/2 ljjz1/2 rzzz rzzl
# from bs4 import BeautifulSoup

BASE_URL = 'http://fund.eastmoney.com/'
FUNDS_PATH1 = 'fund.html#os_0;isall_0;ft_;pt_1'
FUNDS_PATH2 = 'cnjy_jzzzl.html'
CACHE_FILE_NAME1 = 'cacheFunds1.json'
CACHE_FILE_NAME2 = 'cacheFunds2.json'
CACHE_DICT = {}
FUNDS = {}
MANAGER = {}

import json
import time
from bs4 import BeautifulSoup
import requests
import re

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
    response.encoding = "utf-8"
    cache[url] = response.text
    save_cache(cache, filename)
    return cache[url]

# class Funds:
#     def __init__(self, name, jzgs, dwjz, ljjz, lspng, zzl, manager, manager_info):
#         self.name = name
#         self.jzgs = jzgs
#         self.dwjz = dwjz
#         self.ljjz = ljjz
#         self.zzl = zzl
#         self.manager = manager
#         self.manager_info = manager_info



### Webpage 1

CACHE_DICT = load_cache(CACHE_FILE_NAME1)
url = BASE_URL + FUNDS_PATH1
response = make_url_request_using_cache(url, CACHE_DICT, CACHE_FILE_NAME1)
soup = BeautifulSoup(response, 'html.parser')

funds_cache = {}
currentPage_details_path = soup.find_all('td', class_='tol')   #id=re.compile('^tr')
for path in currentPage_details_path[:100]:
    id = path.find('a')['href'][:-5]
    funds_cache[id] = {}
    currentPage_details_url = BASE_URL + id + '.html'

    ##################### Page 2 ######################
    response = requests.get(currentPage_details_url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')
    name = soup.find_all(class_='fundDetail-tit')[0].contents[0].text[:-7]
    details = soup.find_all('div',class_='fundInfoItem')[0].contents
    manager = details[2].contents[1].contents[0].contents[2].contents[1].text
    manager_url = details[2].contents[1].contents[0].contents[2].contents[1]['href']
    dataOfFund = details[1]
    # jzgs = dataOfFund.find(class_='dataItem01').contents[1].text
    temp = dataOfFund.find(class_='dataItem02').contents
    dwjz = temp[1].contents[0].text
    zzl = temp[1].contents[1].text
    ljjz = dataOfFund.find(class_='dataItem03').contents[1].text
    # history_url = temp[0].find('a')['href']
    # response = requests.get(history_url)
    # soup = BeautifulSoup(response.text, 'html.parser')
    # lspng = soup.find('div', class_='listcomm jz_list').find('img')
    # lsjz = soup.find('table', class_='w782 comm lsjz')       # ajax异步获取数据，待解决

    ### page 3
    response = requests.get(manager_url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')
    manager_info = soup.find_all(class_='jl_intro')[0].contents[1].contents[2].text
    manage_funds = soup.find_all(class_='w782 comm jloff')[1].contents[1].contents
    funds_list = []
    for i in manage_funds:
        funds_list.append(i.text[:6])

    MANAGER[manager] = {
        'info': manager_info, 
        'fund': funds_list
        }

    ########## caching ###########
    # funds_cache[id] = Funds(jzgs, dwjz, ljjz, lspng, lsjz, zzl)
    funds_cache[id] = {
        'name': name,
        # 'jzgs': jzgs,
        'dwjz': dwjz,
        'ljjz': ljjz,
        'zzl': zzl,
        'manager': manager
        }

FUNDS['OE'] = funds_cache



### Webpage 2

CACHE_DICT = load_cache(CACHE_FILE_NAME2)
url = BASE_URL + FUNDS_PATH2
response = make_url_request_using_cache(url, CACHE_DICT, CACHE_FILE_NAME2)
soup = BeautifulSoup(response, 'html.parser')

funds_cache = {}
currentPage_details_path = soup.find_all(height='20', id=re.compile('^tr'))   #id=re.compile('^tr')
for path in currentPage_details_path[:100]:
    path = path.find(class_='tl')
    id = path.find('a')['href'][-5-6:-5]
    funds_cache[id] = {}
    currentPage_details_url = BASE_URL + id + '.html'

    ##################### Page 2 #######################
    response = requests.get(currentPage_details_url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')
    name = soup.find_all(class_='fundDetail-tit')[0].contents[0].text[:-7]
    details = soup.find_all('div',class_='fundInfoItem')[0].contents
    manager = details[2].contents[1].contents[0].contents[2].contents[1].text
    manager_url = details[2].contents[1].contents[0].contents[2].contents[1]['href']

    dataOfFund = details[1]
    # jzgs = dataOfFund.find(class_='dataItem01').contents[1].text
    temp = dataOfFund.find(class_='dataItem02').contents
    dwjz = temp[1].contents[0].text
    zzl = temp[1].contents[1].text
    ljjz = dataOfFund.find(class_='dataItem03').contents[1].text
    # history_url = temp[0].find('a')['href']
    # response = requests.get(history_url)
    # soup = BeautifulSoup(response.text, 'html.parser')
    # lspng = soup.find('div', class_='listcomm jz_list').find('img')
    # lsjz = soup.find('table', class_='w782 comm lsjz')


    ### page 3
    response = requests.get(manager_url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')
    manager_info = soup.find_all(class_='jl_intro')[0].contents[1].contents[2].text
    manage_funds = soup.find_all(class_='w782 comm jloff')[1].contents[1].contents
    funds_list = []
    for i in manage_funds:
        funds_list.append(i.text[:6])

    MANAGER[manager] = {
        'info': manager_info,
        'fund': funds_list
        }

    ########## caching ###########
    # funds_cache[id] = Funds(jzgs, dwjz, ljjz, lspng, lsjz, zzl)
    funds_cache[id] = {
        'name': name,
        # 'jzgs': jzgs,
        'dwjz': dwjz,
        'ljjz': ljjz,
        'zzl': zzl,
        'manager': manager
        }

FUNDS['ET'] = funds_cache
save_cache(FUNDS, 'fundsData.json')
save_cache(MANAGER, 'managersData.json')
print(FUNDS)

