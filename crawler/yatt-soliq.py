#link # https://my.soliq.uz/searchtin/index

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import mysql.connector

driver = webdriver.Firefox()

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root",
  database="zerocorruption"
)

mycursor = mydb.cursor()

stirs = []

sql = "SELECT inn from golibs"
mycursor.execute(sql)
myresult = mycursor.fetchall()

l1 = False

for x in myresult:
    stir = x[0]
    url = "https://my.soliq.uz/searchtin/index"
    driver.get(url)
    # https://my.soliq.uz/searchtin/getfio?tin=502299768&captcha=9645 GET
    # captchani yechib YaTT haqida info olish mumkin
    """{
        "tin":"502299768",
        "ns10Name":"XORAZM",
        "ns10NameUz":"XORAZM",
        "ns10NameRu":"ХОРЕЗМСКАЯ",
        "ns11Name":"BOG'OT TUMANI",
        "ns11NameUz":"BOG'OT TUMANI",
        "ns11NameRu":"БАГАТСКИЙ р-н",
        "surName":"YAQUBOV",
        "firstName":"ZAFAR",
        "middleName":"QURBONDURDIYEVICH",
        "tinDate":"29.09.2018",
        "personalNum":"30505793070054",
        "result":"YAQUBOV ZAFAR QURBONDURDIYEVICH",
        "ns13Code":"0",
        "ns13Name":"Фаол"
    }
    """
    #id=tinforfio - stir
    #id=fio_captcha
    #tinforfio = driver.find_element(By.ID,"tinforfio")
    #tinforfio.send_keys(stir)

    # rucaptchadan captchani olish
    # kerak
    # 4 ta raqam
    captcha = "4455"
    url2 = "https://my.soliq.uz/searchtin/getfio?tin=%s&captcha=%s" % (stir,captcha)
    driver.get(url2)
    break