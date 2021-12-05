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
for x in myresult:
    mahsulot = x[6].strip()
    sql = "SELECT id from mahsulots WHERE nom = %s"
    mycursor.execute(sql,(mahsulot,))
    res1 = mycursor.fetchall()
    exists = False
    for a in res1:
        exists = True
    if not exists:
        sql = "INSERT INTO mahsulots(nom) VALUES(%s)"
        mycursor.execute(sql,(mahsulot,))
        mydb.commit()