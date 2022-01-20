import requests
import os.path
import json

for j in range(571):
    fname = "tender_data/" + 'data_' + str(j) + '.json'
    if os.path.isfile(fname):
        print(fname,"is exists")
        continue
    url = "https://tender.mc.uz/apis/api/v1/tenders?page=" + str(j) + "&unique_name=null&name=null&start_price=null&placement_term=null&region_id=null&object_type_id=null&service_type_id=null&status=null&order=created_at"
    resp = requests.get(url)
    print(resp.status_code)
    if resp.status_code == 200:
        js = resp.json()
        data = js['data']
        tenders = data['tenders']['data']
        with open(fname, 'w') as f:
            json.dump(js, f)