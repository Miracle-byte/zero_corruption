#
# neo4j uchun table larni tayyorlash
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
    print(x)