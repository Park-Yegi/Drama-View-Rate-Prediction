from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
import requests
import csv


hdr = {'User-Agent': 'Mozilla/5.0'}
drama_name = '마왕'
url = 'https://search.daum.net/search?w=tv&q='+drama_name +'시청률'

response = requests.get(url, params=hdr)
source = response.text
data = bs(source, 'html.parser')
body = data.find('body')
view_rate_table = body.select('div.detail_wrap > div#tvpColl > div.coll_cont > div.mg_cont > div#tab_content > div#tabCont > div#tv_rating > div.wrap_rank > table.tbl_rank > tbody > tr')
    
if (view_rate_table != None):
    with open('../kbs_each_ep.csv', 'a', encoding='utf-8') as f:
        writer = csv.writer(f)
        
        try:
            for row in view_rate_table:
                broadcasting_date = row.select_one('td').get_text().replace(".", "-")
                episode = int(row.select_one('td > a').get_text().split('회')[0])
                view_rate = float(row.select('td')[2].get_text()[:-1])
                writer.writerow(tuple([drama_name, episode, view_rate, broadcasting_date]))

        except Exception as e:
            print(drama_name)
            print(e)