from selenium import webdriver
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
import requests
import csv

browser = webdriver.Chrome('./chromedriver')
hdr = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36', 'Content-Type': 'application/json; charset=utf-8'}


each_ep = open('../memo.csv', 'w', encoding='utf-8')
ep_wr = csv.writer(each_ep)

drama_name = '푸른거탑'
url = 'https://search.daum.net/search?w=tv&q=%ED%91%B8%EB%A5%B8%EA%B1%B0%ED%83%91%20%EC%8B%9C%EC%B2%AD%EB%A5%A0&irt=tv-program&irk=62342&DA=TVP'
# url = 'https://search.daum.net/search?w=tv&q=%EB%82%98%EC%81%9C%EC%82%AC%EB%9E%91%20%EC%8B%9C%EC%B2%AD%EB%A5%A0&irt=tv-program&irk=87200&DA=TVP'
# response = requests.get(url, params=hdr)
# source = response.text
browser.get(url)
source = browser.page_source
data = bs(source, 'html.parser')
body = data.find('body')
# print(body)
view_rate_table = body.select('div.detail_wrap > div#tvpColl > div.coll_cont > div.mg_cont > div#tab_content > div#tabCont > div#tv_rating > div.wrap_rank > table.tbl_rank > tbody > tr')
# view_rate_table = body.select('div.detail_wrap > div#tvpColl > div.coll_cont > div.mg_cont > div#tab_content > div#tabCont > div > div > table > tbody > tr')
# view_rate_table = body.find('table')
# print(view_rate_table)

if (view_rate_table != None):
    try:
        for row in view_rate_table:
            broadcasting_date = row.select_one('td').get_text().replace(".", "-")
            episode = int(row.select_one('td > a').get_text().split('회')[0])
            view_rate = float(row.select('td')[2].get_text()[:-1])
            ep_wr.writerow(tuple([drama_name, episode, view_rate, broadcasting_date]))
            # ep_wr.writerow(tuple([drama_name, view_rate, broadcasting_date]))
            # print(tuple([drama_name, episode, view_rate, broadcasting_date]))
        print("Finish collecting", drama_name)

    except Exception as e:
        print(drama_name, e)
    
else:
    print(drama_name, "view rate table is None")
    
        
each_ep.close()