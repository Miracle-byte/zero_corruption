import requests
import json
import os.path

for j in range(416):
    fname = "data/" + 'data_' + str(j) + '.json'
    if os.path.isfile(fname):
        print(fname,"is exists")
        continue
    url = "https://tender.mc.uz/apis/api/v1/completed-tenders?page=" + str(j) + "&contract_number=null&unique_name=null&start_price=null&transaction_date=null&region_id=null"
    resp = requests.get(url)
    print(resp.status_code)
    if resp.status_code == 200:
        js = resp.json()
        data = js['data']
        tenders = data['tenders']['data']
        with open(fname, 'w') as f:
            json.dump(js, f)
        for i in range(len(tenders)):
            tender = tenders[i]
            unique_id = tender['unique_id']
            shart_id = tender['id']
            customer = tender['customer']
            winner = tender['winner']
            protocol_url = tender['protocol']
            offer_count = tender['offeror_count']
            region = tender['region']
            print(shart_id,winner)
            resp2 = requests.get(protocol_url)
            with open("pdf/" + str(unique_id) + "_" + str(shart_id) + '.pdf', 'wb') as f:
                f.write(resp2.content)
