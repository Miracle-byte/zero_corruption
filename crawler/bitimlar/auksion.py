# http://xarid.uz/ajax/dxarid?page=2&auction=Stats&status=Completed&year=2021
import requests
from bs4 import BeautifulSoup
import lxml
import mysql.connector
import datetime

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root",
  database="zerocorruption2"
)

mycursor = mydb.cursor()

def existsLotNum(lotnum):
    global mydb
    mycursor = mydb.cursor()
    sql = "SELECT id FROM buyurtmas WHERE lotnum = %s"
    mycursor.execute(sql,(str(lotnum),))
    myresult = mycursor.fetchall()
    ret = False
    for x in myresult:
        ret = True
        break
    mycursor.close()
    return ret

mavjudLotlar = 0

for i in range(1,100):
    url = "http://xarid.uz/ajax/dxarid?page=%d&auction=Stats&status=Completed&year=2021" % (i)
    print(url)
    r = requests.get(url)
    print(r.status_code)
    #print(r.content)
    soup = BeautifulSoup(r.content, 'lxml')
    #print(soup)
    #print(soup.body)
    body = soup.body
    #print(len(body))
    table = soup.find("table", id="pvtTable")
    table_body = table.find('tbody')
    rows = table_body.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        #print(cols)
        print("==========================")
        len1 = len(cols)
        if len1 < 9:
            print("boshqa page qolmadi ishni yakunlaymiz")
            break
        #print(cols[1].text)
        lot1 = cols[1].text.strip()
        start_date = cols[2].text.strip()
        start_date = datetime.datetime.strptime(start_date, "%d.%m.%Y").date()
        end_date = cols[3].text.strip()
        end_date = datetime.datetime.strptime(end_date, "%d.%m.%Y %H:%M:%S").date()
        count = cols[4].text.strip()
        nom = cols[5].text.strip()
        start_narx = cols[6].text.strip().replace("UZS","").replace(" ","").split(',')[0]
        kontrakt_narx = cols[7].text.strip().replace("UZS","").replace(" ","").split(',')[0]
        zakazchik = cols[8].text.strip()
        zakazchik_inn = cols[9].text.strip()
        print(start_narx,kontrakt_narx, zakazchik,zakazchik_inn)
        
        # lot raqamini tekshirish
        if existsLotNum(lot1):
            print(lot1,'bazada mavjud')
            mavjudLotlar = mavjudLotlar + 1
            continue
        # g'olibni olish
        req1 = requests.request(
                method='get', 
                url='http://xarid.uz/ajax/DxaridDealDetails', 
                json={"type": 0, "lotId":lot1} )
                #data='{ "type": 0, "lotId":' + lot1 + '}')
        print(req1.status_code)
        reqjson = req1.json() 
        print(reqjson['items'])
        sql = "INSERT INTO golibs(nom,inn,direktor,tasischi) VALUES(%s,%s,%s,%s)"
        mycursor.execute(sql, (
            reqjson['items'][0]['ProviderName'],
            reqjson['items'][0]['ProviderInn'],
            reqjson['items'][0]['Founder'],
            reqjson['items'][0]['Beneficiary']))
        
        gid = mycursor.lastrowid
        print(gid)
        sql = "INSERT INTO buyurtmas(turi,lotnum,start_date,end_datetime,count,nom,start_narx,end_narx,zakazchik,zakazchik_inn,glid) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        mycursor.execute(sql, ('budjet',lot1,start_date,end_date,int(count),nom,int(start_narx),int(kontrakt_narx),zakazchik,zakazchik_inn,gid))
        
        # ProviderName
        # ProviderInn
        # Founder
        # Beneficiary
        #break
        #for col in cols:
        #    print(col.text)
        #    print("-----------------------------------------")
            
            # http://xarid.uz/ajax/DxaridDealDetails
        #    requests.request(
        #        method='get', 
        #        url='http://xarid.uz/ajax/DxaridDealDetails', 
        #        data='{ "type": 0, "lotId": ' +  }')
    mydb.commit()
    #break

print('barcha mavjud lotlar:',mavjudLotlar)