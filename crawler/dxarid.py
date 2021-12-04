from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import time
import requests

driver = webdriver.Firefox()
# driver.get("https://dxarid.uzex.uz/")
# https://dxarid.uzex.uz/ru/trade/lot/5356270/

url = "https://dxarid.uzex.uz/ru/ajax/filter?LotID=&PriceMin=&PriceMax=&RegionID=&DistrictID=&INN=&CategoryID=&EndDate=03.02.2022&PageSize=1000&Src=AllMarkets&PageIndex=1&Type=trade&Tnved=&StartDate=03.12.2021"
driver.get(url)

time.sleep(3)
tables = driver.find_elements_by_xpath("//table[@class='table_main thead_fixer table_printable']")
#print(tables)
for table in tables:
    print("table-->",table)
    for row in table.find_elements_by_css_selector('tr'):
        cells = row.find_elements_by_tag_name('td')
        len1 = len(cells)
        if len1 == 9:
            id = cells[0].text
            lot = cells[1].text
            enddate = cells[2].text
            reg = cells[3].text
            ray = cells[4].text
            nom = cells[5].text
            cost = cells[6].text
            info = cells[7].text
            print(lot,"|",nom,"|",cost)
            # https://dxarid.uzex.uz/ru/trade/lot/5356270/
            #url1 = 'https://dxarid.uzex.uz/ru/trade/lot/'+lot
            #print(url1)
            #r = requests.get(url1)
            #print(dir(r))
            #print(r.status_code)
            #print(r.content)
            #print(r.headers)
            #driver.close()
            #exit(0)
driver.close()