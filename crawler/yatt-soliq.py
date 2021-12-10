#link # https://my.soliq.uz/searchtin/index

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import time

import mysql.connector
import base64
import requests

# captcha solver
from twocaptcha import TwoCaptcha
solver = TwoCaptcha('d08d1c5c9961953279d92e83ac8ae388')
# result = solver.normal('path/to/captcha.jpg', param1=..., ...)

headers = {
  "User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
}

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
ginns = []
need_get_inns = []

for x in myresult:
  ginns.append(x[0])
sql = "SELECT inn from firmas"
mycursor.execute(sql)
myresult = mycursor.fetchall()
finns = []
for x in myresult:
  finns.append(x[0])

def getGolibFirmaNom(inn):
  global mydb
  mycursor = mydb.cursor()
  sql = "SELECT nom FROM golibs WHERE inn = %s"
  mycursor.execute(sql,(inn,))
  myresult = mycursor.fetchall()
  ret = ""
  for x in myresult:
      ret = x[0]
  mycursor.close()
  return ret

def existsFirmaNom(nom):
  global mydb
  mycursor = mydb.cursor()
  sql = "SELECT id FROM firma_noms WHERE nom = %s"
  mycursor.execute(sql,(nom,))
  myresult = mycursor.fetchall()
  ret = 0
  for x in myresult:
      ret = x[0]
  mycursor.close()
  return ret

def existsRahbar(fio):
    global mydb
    mycursor = mydb.cursor()
    sql = "SELECT id FROM rahbars WHERE fio = %s"
    mycursor.execute(sql,(fio,))
    myresult = mycursor.fetchall()
    ret = 0
    for x in myresult:
        ret = x[0]
    mycursor.close()
    return ret

def existsFirma(inn):
    global mydb
    mycursor = mydb.cursor()
    sql = "SELECT id FROM firmas WHERE inn = %s"
    mycursor.execute(sql,(inn,))
    myresult = mycursor.fetchall()
    ret = 0
    for x in myresult:
        ret = x[0]
    mycursor.close()
    return ret

l1 = False
for x in range(len(ginns)):
    ginn = ginns[x]
    if ginn in finns:
      continue
    
    stir = ginn
    # check ginn is getted
    if existsFirma(stir):
      continue
    if stir.startswith('3'):# or stir.startswith('2'):
      continue 
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
    # 
    cimg = driver.find_elements_by_xpath("//img[@class='img-recaptcha']")
    if len(cimg) > 0:
      img = cimg[0].get_attribute('src').strip()
      if len(img.split(',')) != 2:
        continue
      img = img.split(',')[1]
      #print(img)
      imgdata = base64.b64decode(img)
      filename = 'some_image.jpg'  # I assume you have a way of picking unique filenames
      with open(filename, 'wb') as f:
        f.write(imgdata)
      result = solver.normal(filename)
      #print(result)
      if 'code' in result:
        print('code:',result['code'])
        captcha = result['code'].strip()
        url2 = "https://my.soliq.uz/searchtin/getfio?tin=%s&captcha=%s" % (stir,captcha)
        print(url2)
        driver.find_element_by_link_text("СТИР ёки ЖШШИРингизни текширинг").click()
        tinforfio = driver.find_element(By.ID,"tinforfio")
        tinforfio.send_keys(stir) #
        fio_captcha = driver.find_element(By.ID,"fio_captcha")
        fio_captcha.send_keys(captcha) 
        driver.execute_script("return GetFio();")
        #time.sleep(1)
        fio = driver.find_element(By.ID,"fio")
        director = ""
        while True:
          time.sleep(.1)
          director = fio.get_attribute('value').strip()
          if len(director)>0:
            print(director)
            break
        err1 = "Маълумотлар базасида хеч қандай маълумотлар топилмади!"
        err2 = "Расмдаги матн нотўғри киритилган"
        if director == err1 or director == err2:
          print(stir,"topilmadi, captcha error")
          continue

        # create rahbar
        rahbar_id = existsRahbar(director)
        if rahbar_id == 0:
          # need to create rahbar
          sql = "INSERT INTO rahbars(fio) VALUES(%s)"
          mycursor.execute(sql, (director,))
          mydb.commit()
          rahbar_id = mycursor.lastrowid

        # create firma nom
        firmanom = getGolibFirmaNom(stir)
        firmanom_id = existsFirmaNom(firmanom)
        if firmanom_id == 0:
            sql = "INSERT INTO firma_noms(nom) VALUES(%s)"
            mycursor.execute(sql, (firmanom,))
            mydb.commit()
            firmanom_id = mycursor.lastrowid
        firma_id = existsFirma(stir)
        if firma_id == 0:
            sql = "INSERT INTO firmas(inn,fnomid,rnomid) VALUES(%s,%s,%s)"
            mycursor.execute(sql, (stir,firmanom_id,rahbar_id))
            mydb.commit()
        
        
        #cookies = driver.get_cookies()
        #print(cookies)
        #driver.get(url2)
        #s = requests.session()
        #s.headers.update(headers)
        #for cookie in driver.get_cookies():
        #  print(cookie['name'],cookie['value'])
        #  c = {
        #    cookie['name']: cookie['value']
        #    }
        #  s.cookies.update(c)
        #r = requests.get(url2)
        #print(r.status_code,r.content)
      #break
        
      
      

