from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root",
  database="zerocorruption2"
)
mycursor = mydb.cursor()
driver = webdriver.Firefox()

def innExists(inn):
  global mydb
  mycursor = mydb.cursor()
  sql = "SELECT id FROM stir_htmls WHERE stir = %s"
  mycursor.execute(sql,(str(inn),))
  myresult = mycursor.fetchall()
  ret = 0
  for x in myresult:
    ret = x[0] 
  return ret   

sql = "SELECT * FROM golibs"
mycursor.execute(sql)
buyurtmas = mycursor.fetchall()

for x in buyurtmas:
  try:
    stir = x[2]
    stir = x[2].split('-')[0]
    if len(stir) != 9:
      #sql = "DELETE FROM buyurtmas where id = %s"
      #mycursor.execute(sql, (x[0],))
      continue
    try:
      string_int = int(stir)
      #print(string_int)
    except ValueError:
      print("error parse",stir)
      #sql = "DELETE FROM buyurtmas where id = %s"
      #mycursor.execute(sql, (x[0],))
      continue
    if innExists(stir) > 0:
      print(stir,"--> Exists")
      continue
    url = "http://registr.stat.uz/ext/find_stat.php?OKPO=%s&capcha=kknxzs&send=Ochish&UZ=1" % stir
    print(stir,url)
    driver.get(url)
    demo2 = driver.find_elements_by_xpath("//div[@id='demo2']")
    html = ""
    if len(demo2) > 0:
      html = demo2[0].get_attribute('innerHTML').strip()
    sql = "INSERT INTO stir_htmls(stir,html) VALUES(%s,%s)"
    mycursor.execute(sql, (int(stir),html))
    mydb.commit()
  except:
    pass
    #sql = "DELETE FROM buyurtmas where id = %s"
    #mycursor.execute(sql, (x[0],))  

#mydb.commit()
#driver.close()