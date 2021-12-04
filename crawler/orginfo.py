import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root",
  database="zerocorruption"
)
mycursor = mydb.cursor()
driver = webdriver.Firefox()

sql = "SELECT * from golibs"
mycursor.execute(sql)

myresult = mycursor.fetchall()
l1 = False
for x in myresult:
    print(x[2])
    if len(x[2].split('-')) > 1:
        l1 = True
    if l1 == False:
        continue
    stir = x[2].split('-')[0]
    url = "https://orginfo.uz/search?q=" + stir
    #url = "https://orginfo.uz/search?q=202380828"
    #308509814
    #url = "https://orginfo.uz/search?q=308509814"
    driver.get(url)
    #time.sleep(1)
    # div -- class result-item card bg-dark my-2 p-2 text-left
    card = driver.find_elements_by_xpath("//div[@class='result-item card bg-dark my-2 p-2 text-left']")
    #print(len(card))
    html = ""
    if len(card) > 0:
        card[0].click()
        #time.sleep(1)
        #dl row organization-detail
        #card bg-dark my-2 p-3 text-left
        dl = driver.find_elements_by_xpath("//div[@class='card bg-dark my-2 p-3 text-left']")
        dl = dl[0]
        html = dl.get_attribute('innerHTML').strip()
    sql = "INSERT INTO stir_htmls(stir,html) VALUES(%s,%s)"
    mycursor.execute(sql, (int(stir),html))
    mydb.commit()
    #dl2 = dl.find_elements_by_xpath("//dd")
    #print(dl2)
    #print(len(dl2))
    #for dl3 in dl2:
    #    print(dl3,dl3.text)
driver.close()

