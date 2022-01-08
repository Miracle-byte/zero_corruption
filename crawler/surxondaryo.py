# https://statsnet.co/companies/uz/%D0%A2%D0%90%D0%A8%D0%9A%D0%95%D0%9D%D0%A2?page=
import requests
from bs4 import BeautifulSoup
import lxml
import time

for i in range(10000):
    if i <= 3862:
        continue
    print(i,"Page parsing...") 
    url = "https://statsnet.co/companies/uz/%D0%A1%D0%A3%D0%A0%D0%A5%D0%90%D0%9D%D0%94%D0%90%D0%A0%D0%AC%D0%98%D0%9D%D0%A1%D0%9A%D0%90%D0%AF%20%D0%9E%D0%91%D0%9B%D0%90%D0%A1%D0%A2%D0%AC?page=" + str(i)
    time.sleep(2)
    resp = requests.get(url)
    soup = BeautifulSoup(resp.content, 'lxml')
    #body = soup.body
    for ultag in soup.find_all('ul', {'class': 'space-y-2'}):
        # header ni olamiz
        fnom = ""
        stir = ""
        for h2 in ultag.find_all('h2'):
            #print(h2.text)
            fnom = h2.text
        #
        for p in ultag.find_all('p', {'class': 'text-sm text-gray-500'}):
            if p.text.startswith('БИН'):
                #print(p.text)
                stir = p.text.replace('БИН','').strip()
                print(stir)
                with open("surxondaryo.txt", "a") as myfile:
                    myfile.write(stir+"\n")
        #for litag in ultag.find_all('li'):
        #    print(litag.text)

    #break