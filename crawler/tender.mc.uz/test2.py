import json
import os.path
import requests

for j in range(416):
    fname = "data/" + 'data_' + str(j) + '.json'
    if os.path.isfile(fname):
        f = open(fname)
        js = json.load(f)
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
            with open("D:/hackaton-2021/tender/" + str(unique_id) + "_" + str(shart_id) + '.pdf', 'wb') as f:
                f.write(resp2.content)