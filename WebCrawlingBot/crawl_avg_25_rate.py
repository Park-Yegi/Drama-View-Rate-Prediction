from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
import requests


hdr = {'User-Agent': 'Mozilla/5.0'}
drama_name = '마이 리틀 베이비'
url = 'https://search.daum.net/search?w=tv&q='+drama_name +'시청률'

response = requests.get(url, params=hdr)
source = response.text
data = bs(source, 'html.parser')
body = data.find('body')
view_rate_table = body.select('div.detail_wrap > div#tvpColl > div.coll_cont > div.mg_cont > div#tab_content > div#tabCont > div#tv_rating > div.wrap_rank > table.tbl_rank > tbody > tr')
    
if (view_rate_table != None):
    num_eps = int(view_rate_table[0].select_one('td > a').get_text().split('회')[0])
    num_25 = int(num_eps/4)

    rate_list = []
    try:
        for row in view_rate_table:
            rate_list.append(float(row.select('td')[2].get_text()[:-1]))

        avg_rate = sum(rate_list) / num_eps
        rate_25 = sum(rate_list[:num_25]) / num_25

        print("num_eps: ", num_eps, "avg_rate: ", avg_rate, "rate_25: ", rate_25)
        print(rate_list)
        print(rate_list[:num_25])

    except Exception as e:
        print(drama_name)
        print(e)