from selenium import webdriver
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
import requests

def crawl_view_rate(drama_name):
    hdr = {'User-Agent': 'Mozilla/5.0'}
    url = 'https://search.daum.net/search?w=tv&q='+drama_name +'%20시청률'
    response = requests.get(url, params=hdr)
    source = response.text
    data = bs(source, 'html.parser')
    body = data.find('body')
    print(body)
    view_rate_table = body.select('div.detail_wrap > div#tvpColl > div.coll_cont > div.mg_cont > div#tab_content > div#tabCont > div#tv_rating.tab_count > div.wrap_rank > table.tbl_rank > tbody > tr')
    print(view_rate_table)


if __name__ == "__main__":
    crawl_view_rate('비밀의숲2')