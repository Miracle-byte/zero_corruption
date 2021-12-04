from datetime import datetime
from elasticsearch import Elasticsearch
es = Elasticsearch()

import mysql.connector

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
        'timestamp': end_date,
    }
    res = es.index(index="zero_corruption1", id=rid, document=doc)
    print(res['result'])
    es.indices.refresh(index="zero_corruption1")
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