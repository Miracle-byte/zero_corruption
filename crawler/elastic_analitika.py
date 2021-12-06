from datetime import datetime
from elasticsearch import Elasticsearch
es = Elasticsearch()

import mysql.connector

def getgolibname(inn):
    print("getGolibInn:",inn)
    global mydb
    mycursor = mydb.cursor()
    sql = "SELECT fn.nom FROM firma_noms fn INNER JOIN firmas f on f.fnomid = fn.id and f.inn = %s"
    mycursor.execute(sql,(str(inn),))
    myresult = mycursor.fetchall()
    ret = ""
    for x in myresult:
        ret = x[0]
    mycursor.close()
    return ret

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

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root",
  database="zerocorruption"
)

mycursor = mydb.cursor()
sql = "SELECT * from buyurtmas"
mycursor.execute(sql)

myresult = mycursor.fetchall()
for x in myresult:
    rid = x[0]
    tur = x[1]
    lot = x[2]
    start_date = x[3]
    end_date = x[4]
    count = x[5]
    nom = x[6]
    start_narx = x[7]
    end_narx = x[8]
    zakazchik = x[9]
    zakazchikinn = x[10]
    glid = x[11]
    golibinn = getGolibInn(glid)
    golibfirmaname = getgolibname(golibinn)
    #print(golibfirmaname)
    #exit(0)
    doc = {
        'tur': tur,
        'lot':lot,
        'start_date':start_date,
        #'end_date':end_date,
        'taklif':count,
        'nom':nom,
        'start_narx':start_narx,
        'end_narx':end_narx,
        'zakazchik':zakazchik,
        'zakazchikinn':zakazchikinn,
        'golibinn':golibinn,
        'golibnomi':golibfirmaname,
        'timestamp': end_date,
    }
    res = es.index(index="zero_corruption2", id=rid, document=doc)
    print(res['result'])
    es.indices.refresh(index="zero_corruption2")
    # golib_name = ""
    # golib_inn = 0
    #print(x)

#doc = {
#    'author': 'kimchy',
#    'text': 'Elasticsearch: cool. bonsai cool.',
#    'timestamp': datetime.now(),
#}
#res = es.index(index="test-index", id=1, document=doc)
#print(res['result'])
#
#res = es.get(index="test-index", id=1)
#print(res['_source'])
#
#es.indices.refresh(index="test-index")
#
#res = es.search(index="test-index", query={"match_all": {}})
#print("Got %d Hits:" % res['hits']['total']['value'])
#for hit in res['hits']['hits']:
#    print("%(timestamp)s %(author)s: %(text)s" % hit["_source"])