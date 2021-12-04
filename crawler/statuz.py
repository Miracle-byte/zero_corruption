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

sql = "SELECT stir FROM stir_html3s"
mycursor.execute(sql)
myresult = mycursor.fetchall()
stirs = []
for x in myresult:
    stirs.append(x[0])

sql = "SELECT zakazchik_inn from buyurtmas"
mycursor.execute(sql)

myresult = mycursor.fetchall()

for x in myresult:
    stir = x[0]
    if int(stir) in stirs:
        print(stir,"exists")
        continue
    else:
        print(stir)
    # undan oldin
    url = "http://registr.stat.uz/ext/find_stat.php?OKPO=%s&capcha=xsumhi&send=Ochish&UZ=1" % stir
    print(stir,url)
    driver.get(url)
    #time.sleep(1)
    #OKPO
    #okro = driver.find_element_by_css_selector("input[name='OKPO']")
    #okro = driver.find_element_by_name('OKPO')
    #print(okro)
    #okro.send_keys(stir)
    #demo2
    demo2 = driver.find_elements_by_xpath("//div[@id='demo2']")
    #print(len(card))
    html = ""
    if len(demo2) > 0:
        html = demo2[0].get_attribute('innerHTML').strip()
    sql = "INSERT INTO stir_html3s(stir,html) VALUES(%s,%s)"
    mycursor.execute(sql, (int(stir),html))
    mydb.commit()
    break

#driver.close()