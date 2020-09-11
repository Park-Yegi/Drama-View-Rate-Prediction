from selenium import webdriver
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
import requests
import hashlib

def search_news(drama_name):
    links = []
    hdr = {'User-Agent': 'Mozilla/5.0'}
    url = 'https://search.naver.com/search.naver?where=news&sm=ent_nex&ie=utf8&query='+drama_name
    # browser = webdriver.Chrome('./chromedriver')
    # browser.get(url)
    response = requests.get(url, params=hdr)
    # source = browser.page_source
    source = response.text
    data = bs(source, 'html.parser')
    body = data.find('body')
    a_tags = body.select('div#wrap > div#container > div#content > div#main_pack > div.news.mynews.section._prs_nws > ul.type01 > li > dl > dd.txt_inline > a._sp_each_url')
    for a_tag in a_tags:
        links.append(a_tag.attrs['href'])
    # print(links)
    return links


def get_each_news(links):
    browser = webdriver.Chrome('./chromedriver')
    for link in links:
        browser.get(link)
        # hdr = {'User-Agent': 'Mozilla/5.0'}
        # response = requests.get(link, params=hdr)
        source = browser.page_source
        # source = response.text
        data = bs(source, 'html.parser')
        body = data.find('body')
        main = body.select_one('div#wrap > div#content > div.end_ct > div.end_ct_area')
        
        if (main != None):
            # print(link)
            url_hash = hashlib.sha256(link.encode()).hexdigest()
            title = main.select_one('h2.end_tit').get_text().strip()
            written_time = main.select_one('div.article_info > span.author > em').get_text()
            body_text = main.select_one('div.end_body_wrp > div#articeBody').get_text().strip()
            recommends = main.select_one('div.end_btn > div.tomain.as_addinfo > div#toMainContainer > a > em.u_cnt._count').get_text()
            # print(url_hash)
            # print(title)
            # print(written_time)
            print(body_text)
            # print(recommends)


if __name__ == "__main__":
    links = search_news('비밀의숲')
    get_each_news(links)
