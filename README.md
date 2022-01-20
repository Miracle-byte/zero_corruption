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
    
    MATCH (n:Rahbar{fio:'XALMURADOV RUSTAM IBRAGIMOVICH'}) RETURN n LIMIT 25
    MATCH (n:Rahbar{fio:'ESHMATOV FARXOD TO‘XTAMURODOVICH'}) RETURN n LIMIT 25
    MATCH (n:Rahbar{fio:'FURQATOV RUSTAM FURQATOVICH'}) RETURN n LIMIT 25

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

07-12-2021
==========

# my.soliq.uz dan STIR orqali YATT rahbarini olish



09-12-2021
==========

# PF-5729
## O‘ZBEKISTON RESPUBLIKASIDA KORRUPSIYAGA QARSHI KURASHISH TIZIMINI YANADA TAKOMILLASHTIRISH CHORA-TADBIRLARI TO‘G‘RISIDA
    sud
        sudyalarga har qanday tarzda qonunga xilof ravishda ta’sir o‘tkazish shart-sharoitlarini istisno etish
        sud hokimiyatining mustaqilligini yanada mustahkamlash
    
    davlat xizmatchilari daromadlarini deklaratsiya qilish
    davlat xizmatchilarini tanlov asosida saralab olish

    idoraviy korrupsiyaga qarshi kurashishning samarali dasturlarini amalga oshirish

    korrupsiya xavf-xatariga eng ko‘p duch keladigan davlat xizmatchilarining faoliyat sohalari va lavozimlari, shuningdek, ularning funksiyalari (vakolatlari)ning ro‘yxatini shakllantiradi


### affillangan shaxslarning


# uzex dxarid exarid
    dan barcha faol lot larni olish ularni ichidagi har bir maxsulotni analiz qilib chiqish


10-12-2021
==========

## neo4j queries
    MATCH (m:Mahsulot{nom:"ТМЗ"}),(m)<--(bs:Buyurtma3S),(bs)-->(f:Firma{inn:"304507685"}),(f)-->(t:Tasischi),(r:Rahbar)<--(f),(fn:FirmaNom)<--(f),(b:Buyurtma{turi:"budjet"})<--(bs) RETURN *
    
## O'zgarishlar
    G'olib firmalar
    Zakazchik firmalar



11-12-2021
==========

## TASHKILOTLARNING MASʼUL HODIMLARI 
    https://project.gov.uz/oz/site/login

## neo4j Bloom

## БЮДЖЕТ ХАРИДЛАР
    http://xarid.uz/dxarid/deals?status=Completed&auction=Stats


    http://xarid.uz/dxarid/deals
    https://etender.uzex.uz/home

13-12-2021
==========


## Python bilan olingan ma'lumotlarni neo4j ga kiritmoqdamiz

30-12-2021
==========

http://openid.uzex.uz/Files/instructoin_ru.docx

dxarid.uzex.uz
exarid.uzex.uz
shop.uzex.uz
eshop.uzex.uz
millidokon.uzex.uz
emilliydokon.uzex.uz

01-01-2022
===========

#### Firmalar haqida qo'shimcha ma'lumotlar
    https://statsnet.co/companies/uz/%D0%A2%D0%90%D0%A8%D0%9A%D0%95%D0%9D%D0%A2?page=1

#### kerakli infolarni olish:
    MATCH(b:Bitim) MATCH(b)--(g:Golib) MATCH (b)--(z:Zakazchik) MATCH (z)--(zr:ZakazchikRahbar) MATCH (g)--(t:Tasischi) MATCH (z)--(t) MATCH(m:Mahsulot)--(b) MATCH (gr:GolibRahbar)--(g) RETURN * ORDER BY b.start_narx DESC LIMIT 10 



20-01-2022
===========

“Давлат харидлари тўғрисида”ги қонуннинг 42-моддасига кўра, давлат харидларида аффилланганлик ҳолатлари аниқланса, харид иштирокчиси жараёндан четлатилиши лозим.