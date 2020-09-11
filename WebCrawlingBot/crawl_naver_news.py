from selenium import webdriver
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
import requests
import hashlib
import MySQLdb

def connect_to_db(drama_name):
    global connection
    global cursor

    connection = MySQLdb.connect(
        user="scrapingman",
        passwd="myPassword-1",
        host="localhost",
        db="scrapingdata",
        charset="utf8")

    cursor=connection.cursor()

    drama_id = cursor.execute("SELECT id from drama_info where drama_name = %s", [drama_name])
    return drama_id


def unconnect_to_db():
    connection.commit()
    connection.close()


def search_news(drama_name, drama_id):
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


def get_each_news(links, drama_id):
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
            recommends = int(main.select_one('div.end_btn > div.tomain.as_addinfo > div#toMainContainer > a > em.u_cnt._count').get_text())
            # print(url_hash)
            # print(title)
            # print(written_time)
            # print(body_text)
            # print(recommends)
            written_time = written_time.replace('.', '-', 2).replace('.', "") + ":00"
            timestamp_list = written_time.split(' ')
            if (timestamp_list[1] == "오후"):
                time_list = timestamp_list[2].split(":")
                time_list[0] = str(int(time_list[0])+12)
                timestamp_list[2] = ":".join(time_list)
                
            written_time = timestamp_list[0] + ' ' + timestamp_list[2]
            news_tuple = (drama_id, url_hash, title, written_time, body_text, recommends)

            try:
                cursor.execute("INSERT INTO naver_news(id, url_hash, title, modified_time, body_text, recommends) values (%s, %s, %s, %s, %s, %s)", news_tuple)
            except Exception as e:
                print(e)


if __name__ == "__main__":
    drama_name = "비밀의숲2"
    drama_id = connect_to_db(drama_name)
    links = search_news(drama_name, drama_id)
    get_each_news(links, drama_id)
    unconnect_to_db()
