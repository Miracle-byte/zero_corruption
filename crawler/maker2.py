#
# neo4j uchun table larni tayyorlash
# mahsulotlar tablitsasi uchun
#

import mysql.connector


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root",
  database="zerocorruption"
)
mycursor = mydb.cursor()

sql = "SELECT * FROM buyurtmas"
mycursor.execute(sql)
myresult = mycursor.fetchall()

def getGolibInn(inn):
    print("getGolibInn:",inn)
    global mydb
    mycursor = mydb.cursor()
    sql = "SELECT inn FROM golibs WHERE id = %s"
    mycursor.execute(sql,(str(inn),))
    myresult = mycursor.fetchall()
    ret = 0
    for x in myresult:
        ret = x[0]
    mycursor.close()
    return ret

def getFirmaId(inn):
    global mydb
    print("getFirmaId:",inn)
    mycursor = mydb.cursor()
    sql = "SELECT id FROM firmas WHERE inn = %s"
    mycursor.execute(sql,(str(inn),))
    myresult = mycursor.fetchall()
    ret = 0
    for x in myresult:
        ret = x[0]
    mycursor.close()
    return ret


for x in myresult:
    mahsulot = x[6].strip()
    sql = "SELECT id from mahsulots WHERE nom = %s"
    mycursor.execute(sql,(mahsulot,))
    res1 = mycursor.fetchall()
    mah_id = 0
    for a in res1:
        mah_id = a[0]
    buyurtma_id = x[0]
    golib_id = getFirmaId(getGolibInn(x[11]))
    print(x[10])
    zakazchik_id = getFirmaId(x[10])
    sql = "INSERT INTO buyurtma4s(lot_id,mahid,buyurtmaid,golibid) VALUES(%s,%s,%s)"
    print((mah_id,buyurtma_id,zakazchik_id,golib_id))
    if golib_id != 0:
        mycursor.execute(sql,(mah_id,buyurtma_id,golib_id))

mydb.commit()