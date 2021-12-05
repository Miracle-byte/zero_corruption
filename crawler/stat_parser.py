import mysql.connector
from bs4 import BeautifulSoup
import lxml

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root",
  database="zerocorruption"
)

mycursor = mydb.cursor()
sql = "SELECT stir,html FROM stir_html3s"
mycursor.execute(sql)
myresult = mycursor.fetchall()

def existFirmaNom(nom):
    pass

def existRahbar(fio):
    pass

def 
for x in myresult:
    stir = x[0]
    if len(x[1].strip()) == 0:
        continue
    soup = BeautifulSoup(x[1], 'lxml')
    body = soup.body
    table = soup.find("table")
    table_body = table.find('tbody')
    rows = table_body.find_all('tr')
    #print(len(rows))
    isTasischi = False
    isBoshqaruvchi = False
    nom = ""
    inn = ""
    rahbar = ""
    tasischilar = []
    for row in rows:
        cols = row.find_all('td')
        len1 = len(cols)
        field = cols[0].text
        #print(cols)
        if len1 == 1:
            if 'ularning ustav fondidagi' in field:
                isTasischi = True
            elif isTasischi:
                isTasischi = False
            if 'Boshqaruvchi haqida' in field:
                #print(field)
                isBoshqaruvchi = True
        elif len1 == 2:
            a1 = cols[1].text
            if isTasischi:
                foiz = a1
                #print(inn,"nom:",nom,"foiz:",foiz,"rahbar:",rahbar)
                tasischilar.append((field,foiz))
            elif "INN" in field:
                inn = a1.strip()
            elif "Rahbarning F.I.SH" in field:
                rahbar = a1.strip()
            elif "Yuridik shaxsning nomi" in field:
                # mas`uliyati cheklangan jamiyati
                # mas'uliyati cheklangan jamiyati
                # Mas`uliyati cheklangan jamiyati
                # Mas'uliyati cheklangan jamiyat
                # Mas‘uliyati cheklangan jamiyati
                nom = a1.strip().replace("mas‘uliyati cheklangan jamiyati","MChJ")
                nom = nom.replace("mas`uliyati cheklangan jamiyati","MChJ")
                nom = nom.replace("mas'uliyati cheklangan jamiyati","MChJ")
                nom = nom.replace("Mas`uliyati cheklangan jamiyat","MChJ")
                nom = nom.replace("Mas'uliyati cheklangan jamiyat","MChJ")
                nom = nom.replace("Mas‘uliyati cheklangan jamiyat","MChJ")
                if "cheklangan" in nom:
                    print(nom)
    #print("nom:",nom)
    fish = rahbar.split(' ')
    if len(fish)>=2:
        fam = fish[1].strip()
        ism = fish[0].strip()
        shar = ""
        for i in range(2,len(fish)):
            shar = shar + " " + fish[i].strip()
        shar = shar.strip()
        rahbar = fam + " " + ism + " " + shar
    # firma nomini insert qilamiz
    # rahbarni insert qilamiz
    # firmani insert qilamiz
    #print("inn:",inn,"rahbar:",rahbar)
    for i in range(len(tasischilar)):
        t = tasischilar[i]
        fnom = t[0].split('.')[1].strip()
        foiz = t[1]
        # har bir tasischilarni insert qilamiz
        #print(tasischilar[i])
        #print("Ta'sischi:",i+1,"-fnom:",fnom,"foiz:",foiz)
    #print("=========================")
mydb.commit()