from neo4j import GraphDatabase

import mysql.connector

# like query in cypher
# MATCH (gr:GolibRahbar) Where gr.fio =~ '.*MIROD.*' RETURN gr LIMIT 10
mydb = mysql.connector.connect(
  host="192.168.0.104",
  user="test1",
  password="test1",
  database="zerocorruption2"
)
mycursor = mydb.cursor()

sql = "SELECT * FROM buyurtmas"

mycursor.execute(sql)
myresult = mycursor.fetchall()

sql = "SELECT * FROM golibs"
mycursor.execute(sql)
golibs = mycursor.fetchall()

######
sql = "SELECT * FROM firmas"
mycursor.execute(sql)
firmas = mycursor.fetchall()

sql = "SELECT * FROM firma_noms"
mycursor.execute(sql)
firma_noms = mycursor.fetchall()

sql = "SELECT * FROM rahbars"
mycursor.execute(sql)
rahbars = mycursor.fetchall()

sql = "SELECT * FROM tasischis"
mycursor.execute(sql)
tasischis = mycursor.fetchall()

sql = "SELECT * FROM firma_tasischis"
mycursor.execute(sql)
firma_tasischis = mycursor.fetchall()

# delete all things from database
# MATCH (n) DETACH DELETE n
# MERGE bilan faqat 1 kopiya yaratish uchun
if __name__ == "__main__":
    driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "test2"), encrypted=False)
    session = driver.session()
    #i = 10
    for x in myresult:
        print(x)
        golib = None 
        for y in golibs:
            if y[0] == x[11]:
                golib = y
                break
        
        lotnum =x[2]
        mahsulotnom = x[6]

        zakazchiknom = x[9]
        zakazchikinn = x[10]

        golibinn = golib[2]
        golibnom = golib[1]
        
        golibFirma = None
        for f in firmas:
            if f[1] == golibinn:
                golibFirma = f
                break
        
        if golibFirma == None:
            print("golibFirma is not found",golibinn)
            continue

        zakazchikFirma = None 
        for f in firmas:
            if f[1] == zakazchikinn:
                zakazchikFirma = f
                break

        if zakazchikFirma == None:
            print("zakazchik is not found",zakazchikinn)
            continue
        
        zakazchikFirmaNom = None
        golibFirmaNom = None

        for fn in firma_noms:
            if fn[0] == zakazchikFirma[2]:
                zakazchikFirmaNom = fn[1]
            if fn[0] == golibFirma[2]:
                golibFirmaNom = fn[1] 
        
        zakazchikRahbarNom = None
        golibFirmaRahbar = None
        for r in rahbars:
            if r[0] == zakazchikFirma[3]:
                zakazchikRahbarNom = r[1]
            if r[0] == golibFirma[3]:
                golibFirmaRahbar = r[1]
        
        result = session.run("""
                MERGE(m:Mahsulot{nom:$mnom}) 
                MERGE(b:Bitim{lotnum:$lotnum})
                MERGE(z:Zakazchik{nom:$znom,inn:$zinn})
                MERGE(zr:ZakazchikRahbar{fio:$zrfio})
                MERGE(g:Golib{nom:$gnom,inn:$ginn})
                MERGE(gr:GolibRahbar{fio:$grfio})""",
            lotnum=lotnum,mnom=mahsulotnom,
            znom=zakazchikFirmaNom,zinn=zakazchikinn,zrfio=zakazchikRahbarNom,
            gnom=golibFirmaNom,ginn=golibinn,grfio=golibFirmaRahbar)
        
        # MERGE(zr:ZakazchikRahbar{fio:$zrfio})
        # MERGE(gr:GolibRahbar{fio:$grfio})
        # result = session.run("""""")
        result = session.run("""
                MATCH(m:Mahsulot{nom:$mnom}) 
                MATCH(b:Bitim{lotnum:$lotnum}) 
                MERGE (m)-[:MAHSULOT]->(b)""",
            mnom=mahsulotnom,lotnum=x[2])

        result = session.run("""
                MATCH(b:Bitim{lotnum:$lotnum}) 
                MATCH(z:Zakazchik{nom:$znom,inn:$zinn}) 
                MATCH(g:Golib{nom:$gnom,inn:$ginn}) 
                MERGE (g)<-[:GOLIB]-(b)-[:ZAKAZCHIK]->(z)""",
            lotnum=lotnum,znom=zakazchikFirmaNom,zinn=zakazchikinn,gnom=golibFirmaNom,ginn=golibinn)
        
        result = session.run("""
                MATCH(z:Zakazchik{nom:$znom,inn:$zinn})
                MATCH(zr:ZakazchikRahbar{fio:$zrfio})
                MERGE (z)<-[:RAHBAR]-(zr)""",
            znom=zakazchikFirmaNom,zinn=zakazchikinn,zrfio=zakazchikRahbarNom)

        result = session.run("""
                MATCH(g:Golib{nom:$gnom,inn:$ginn})
                MATCH(gr:GolibRahbar{fio:$grfio})
                MERGE (g)<-[:RAHBAR]-(gr)""",
            gnom=golibFirmaNom,ginn=golibinn,grfio=golibFirmaRahbar)
        #i = i - 1
        #if i == 0 :
        #    break
    session.close()
    driver.close()

# MATCH (g:Golib)<--(gr:GolibRahbar) WITH gr,count(g) as cnt WHERE cnt > 1 RETURN *

# MATCH (b:Bitim)<--(m:Mahsulot) MATCH (b)-->(g:Golib) MATCH (g)<--(gr:GolibRahbar) MATCH (b)-->(z:Zakazchik) 
# MATCH (z)<--(zr:ZakazchikRahbar) WITH split(zr.fio,' ') as zrsplit,split(gr.fio,' ') as grsplit,b,g,z,zr,gr 
# WHERE gr.fio =~ "ABDULLA.*" and zr.fio =~ "ABDULLA.*" RETURN *

# MATCH (b:Bitim)<--(m:Mahsulot) MATCH (b)-->(g:Golib) MATCH (g)<--(gr:GolibRahbar) 
# MATCH (b)-->(z:Zakazchik) MATCH (z)<--(zr:ZakazchikRahbar) WITH split(zr.fio,' ') as zrsplit,
# split(gr.fio,' ') as grsplit,b,g,z,zr,gr WHERE zrsplit[0]=grsplit[0] and zrsplit[2]=grsplit[2] RETURN *