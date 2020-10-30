from selenium import webdriver
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
import requests
import csv

browser = webdriver.Chrome('./chromedriver')
hdr = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36', 'Content-Type': 'application/json; charset=utf-8'}

all_drama = open('../last_drama.csv', 'r', encoding='utf-8')
each_ep = open('../two_each_ep.csv', 'w', encoding='utf-8')
drama_rdr = csv.reader(all_drama)
ep_wr = csv.writer(each_ep)

for drama in drama_rdr:
    drama_name = drama[0]
    # url = 'https://search.daum.net/search?w=tv&q='+drama_name +'시청률'
    url = 'https://search.daum.net/search?w=tv&q=' + drama_name+ ' 시청률&irt=tv-program&DA=TVP'
    # response = requests.get(url, params=hdr)
    # source = response.text
    browser.get(url)
    source = browser.page_source
    data = bs(source, 'html.parser')
    body = data.find('body')
    view_rate_table = body.select('div.detail_wrap > div#tvpColl > div.coll_cont > div.mg_cont > div#tab_content > div#tabCont > div#tv_rating > div.wrap_rank > table.tbl_rank > tbody > tr')
        
    if (view_rate_table != None):
        try:
            if int(view_rate_table[0].select_one('td > a').get_text().split('회')[0]) != int(drama[7]):
                print(drama_name, 'End date is not same')
                continue

            for row in view_rate_table:
                broadcasting_date = row.select_one('td').get_text().replace(".", "-")
                episode = int(row.select_one('td > a').get_text().split('회')[0])
                view_rate = float(row.select('td')[2].get_text()[:-1])
                ep_wr.writerow(tuple([drama_name, episode, view_rate, broadcasting_date]))
            print("Finish collecting", drama_name)

        except Exception as e:
            print(drama_name, e)
    
    else:
        print(drama_name, "view rate table is None")
    
        
all_drama.close()
each_ep.close()