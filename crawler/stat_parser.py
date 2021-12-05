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

def existsTasischi(nom):
    global mydb
    mycursor = mydb.cursor()
    sql = "SELECT id FROM tasischis WHERE nom = %s"
    mycursor.execute(sql,(nom,))
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
                tasischilar.append((field.upper(),foiz))
            elif "INN" in field:
                inn = a1.strip()
            elif "Rahbarning F.I.SH" in field:
                rahbar = a1.strip().upper()
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
                #if "cheklangan" in nom:
                #    print(nom)
                nom = nom.upper()
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
    firmanom_id = existsFirmaNom(nom)
    if firmanom_id == 0:
        sql = "INSERT INTO firma_noms(nom) VALUES(%s)"
        mycursor.execute(sql, (nom,))
        mydb.commit()
        firmanom_id = mycursor.lastrowid
    # rahbarni insert qilamiz
    rahbarfio_id = existsRahbar(rahbar)
    if rahbarfio_id == 0:
        sql = "INSERT INTO rahbars(fio) VALUES(%s)"
        mycursor.execute(sql, (rahbar,))
        mydb.commit()
        rahbarfio_id = mycursor.lastrowid 
    # firmani insert qilamiz
    firma_id = existsFirma(inn)
    if firma_id == 0:
        sql = "INSERT INTO firmas(inn,fnomid,rnomid) VALUES(%s,%s,%s)"
        mycursor.execute(sql, (inn,firmanom_id,rahbarfio_id))
        mydb.commit()
        firma_id = mycursor.lastrowid
        #print("inn:",inn,"rahbar:",rahbar)
        for i in range(len(tasischilar)):
            t = tasischilar[i]
            fnom = t[0].split('.')[1].strip()
            foiz = t[1]
            tasischi_id = existsTasischi(fnom)
            if tasischi_id == 0:
                sql = "INSERT INTO tasischis(nom) VALUES(%s)"
                mycursor.execute(sql, (fnom,))
                mydb.commit()
                tasischi_id = mycursor.lastrowid
            sql = "INSERT INTO firma_tasischis(fid,tid,ulush) VALUES(%s,%s,%s)"   
            mycursor.execute(sql, (firma_id,tasischi_id,foiz))
            mydb.commit()
            # har bir tasischilarni insert qilamiz
            #print(tasischilar[i])
            #print("Ta'sischi:",i+1,"-fnom:",fnom,"foiz:",foiz)
    print("=========================")
mydb.commit()