# zero_corruption
datahack.uz antikorrupsiya uchun loyiha.

02-12-2021
==========

# https://anticorruption.uz/uz/item/2021/12/02/xalqaro-press-klub-ozbekistonda-aksilkorrupsiyaviy-islohotlar-mavjud-muammolar-va-istiqboldagi-rejalar

# Akmal Burxonov
    budjet mablag'larining maqsadsiz sarflanishi
    turli talon-tarojlikka yo'l qo'yilish
    d.xarid.uz
    data.gov.uz
    my.gov.uz

# https://www.transparency.org/en
    Transparency International - mamlakatlar korrupsiya holatini baholab beruvchi butunjahon site


# farmatsevtika bo'yicha
    https://anticorruption.uz/uz/item/2021/05/19/ssv-huzuridagi-farmatsevtika-tarmogini-rivojlantirish-agentligida-otkazilgan-organish-natijalari-yuzasidan


# https://lex.uz/docs/-4355387
    budjet mablag'larining maqsadsiz sarf qilinishi
    o'zlashtirish va talon-toroj qilish holatlari
    aslida ishlamagan xodimlar uchun oylik ish haqlari to�lab kelinishi
    budjetga soliqlarning to'lanmaganligi
    davlat xaridlari jarayonlari o'tkazilishi
    bir qator dori vositalari va tibbiy buyumlar sifatida e�tirof etilmaydigan preparatlarni normativ talablarga zid ravishda dori vositasida davlat ro�yxatidan o�tkazilganligi kabi qator qonun buzilishi holatlari aniqlandi.


# PF-5729
    komissiya tashkil etish
    davlat xizmatchilarini tanlov asosida lavozimga tayinlash
    davlat xizmatchilari daromadlarini deklaratsiya qilish
    davlat organlari va tashkilotlarining hisobdorligi va faoliyatining shaffofligini oshirish

# Korrupsiyasi soha
    Sud 
    Prokuratura 
    Soliq 
    Sog'liqni saqlash


03-11-2021
==========

# ochiq budjet haqida ma'lumotlar
    https://openbudget.uz/


# O‘RQ-419 
    https://lex.uz/docs/-3088008

# https://eanticor.uz/uz/
# https://data.egov.uz/rus
# https://reestr.uz/uz

# STIR bo'yicha 
    http://registr.stat.uz/enter_form/index.php

# Completed lot lar bo'yicha
    http://xarid.uz/dxarid/deals?status=Completed


# Korrupsiya bo'yicha risklarni baholash
    Neo4j Desktop orqali baholash
    relationshiplarni hosil qilish

04-12-2021
==========

# Korrupsiya bo'lishi ehtimoli
    Pora olish-berish bilan kurashish siyosati
    Boshqaruv organi, majburiyat va mas’uliyat
    Xodimlarni nazorat qilish va o‘qitish
    Xatarlarni baholash
    Loyihalar va biznes hamkorlarni kompleks tekshirish
    Moliyaviy, tijoriy va shartnomaviy nazorat
    Hisobot, monitoring, surishtirish va umumiy tahlil
    To‘g‘rilovchi harakatlar va doimiy yaxshilash


05-12-2021
==========

# stat.uz dan firma lar haqida nomlar parse qilindi

# Neo4j da svyazkalarni hosil qilish

# Korrupsiyaga oid indeks
    https://gtmarket.ru/ratings/corruption-perceptions-index


# Cypher so'rovlari
    MATCH (t:Tasischi)<--(f:Firma)-->(fn:FirmaNom) RETURN t,f,fn LIMIT 20


06-12-2021
==========

# daryo.uz
    https://daryo.uz/2021/12/06/toshkentda-bosh-prokuratura-mansabdori-29-ming-dollar-pora-olayotganda-qolga-tushdi/
    
# MATCH (n:Rahbar{fio:'XALMURADOV RUSTAM IBRAGIMOVICH'}) RETURN n LIMIT 25
# MATCH (n:Rahbar{fio:'ESHMATOV FARXOD TO‘XTAMURODOVICH'}) RETURN n LIMIT 25
# MATCH (n:Rahbar{fio:'FURQATOV RUSTAM FURQATOVICH'}) RETURN n LIMIT 25

# Learning Cypher
    MATCH (n:Person)-[r*1..3]->(m:Person) RETURN *
    MATCH (n:Person) WHERE n.age < 30 RETURN n.name, n.age
    MATCH (n:Person)-[k:KNOWS]->(f) WHERE k.since < 2000 RETURN f.name, f.age, f.email
    WITH 'AGE' AS propname MATCH (n:Person) WHERE n[toLower(propname)] < 30 RETURN n.name, n.age
    MATCH (n:Person) WHERE n.belt IS NOT NULL RETURN n.name, n.belt
    MATCH (n:Person) WHERE n.name STARTS WITH 'Pet' RETURN n.name, n.age
    MATCH (n:Person) WHERE n.name ENDS WITH 'ter' RETURN n.name, n.age
    MATCH (n:Person) WHERE n.name CONTAINS 'ete' RETURN n.name, n.age

    MATCH (p:PERSON)-[:LIVES]->(c:CITY) WITH p,count(c) as rels, collect(c) as cities WHERE rels > 1 RETURN p,cities, rels

    MATCH (t:Tasischi)<--(f:Firma) with t,count(f) as cnt,collect(f) as cnt1  where cnt > 10 RETURN * LIMIT 25

    MATCH (t:Tasischi)<--(f:Firma)-->(r:Rahbar) with count(t) as cnt,f,r,collect(t) as cnt1  where cnt > 1 RETURN * LIMIT 25

# bitta rahbarning 1 dan ortiq firmasi bo'lsa shularni chiqarish
    MATCH (r:Rahbar)<--(f:Firma) with count(f) as cnt,r,collect(f) as cnt1 where cnt > 1 RETURN * 