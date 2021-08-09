from selectorlib import Extractor
import requests
from time import sleep
import csv
headers = {
'Connection': 'keep-alive',
'Pragma': 'no-cache',
'Cache-Control': 'no-cache',
'DNT': '1',
'Upgrade-Insecure-Requests': '1',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
'Referer': 'https://www.booking.com/index.en-gb.html',
'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8'
}
e = Extractor.from_yaml_file('bookings.yml')
s = Extractor.from_yaml_file('site.yml')
def scrape(url):
    r = requests.get(url, headers=headers)
    return e.extract(r.text, base_url=url)

print("Enter Query url: ")
url = input()
with open('data.csv','w') as outfile:
    fieldnames = ["name", "start_date", "end_date", "room_type", "price", "link"]
    writer = csv.DictWriter(outfile, fieldnames=fieldnames,quoting=csv.QUOTE_ALL)
    writer.writeheader()
    data = scrape(url)
    if data:
        for i in data['hotels']:
            i['name'] = str(i['name'][0])
            i['link'] = str(i['link'][0])
            r = requests.get(i['link'], headers = headers)
            data_site = s.extract(r.text, base_url=i['link'])
            c = 0
            i['start_date'] = data_site['start_date']
            i['end_date'] = data_site['end_date']
            for k in range(len(data_site['type'])):
                i['room_type'] = data_site['type'][k]
                for l in range(int(data_site['Number'][k])):
                    i['price'] = data_site['price'][c]
                    i['price'] = i['price'][2:]
                    i['price'] = str(i['price'])
                    c += 1
                    writer.writerow(i)
