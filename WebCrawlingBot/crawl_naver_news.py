from selenium import webdriver
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
import requests
import hashlib
import MySQLdb
import pymysql
import TimeoutException
import signal

def connect_to_db():
    global connection
    global cursor

    connection = MySQLdb.connect(
        user="scrapingman",
        passwd="myPassword-1",
        host="localhost",
        db="scrapingdata",
        charset="utf8")

    cursor=connection.cursor()


def unconnect_to_db():
    connection.commit()
    connection.close()


def search_news(drama_name, drama_id, start):
    try:
        print("===== Search naver news ", drama_name, " pageNo=", start, " =====")
        links = []
        hdr = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36', 'Content-Type': 'application/json; charset=utf-8'}

        url = 'https://search.naver.com/search.naver?&where=news&query=' + drama_name +'&sm=tab_pge&sort=0&start=' + str(start)
        response = requests.get(url, params=hdr)
        source = response.text
        data = bs(source, 'html.parser')
        body = data.find('body')
        a_tags = body.select('div#wrap > div#container > div#content > div#main_pack > div.news.mynews.section._prs_nws > ul.type01 > li > dl > dd.txt_inline > a._sp_each_url')
        for a_tag in a_tags:
            links.append(a_tag.attrs['href'])
    
    except Exception as e:
        print(e)
    
    return links


def sql_datetime_form(written_time):
    new_written_time = written_time.replace('.', '-', 2).replace('.', "") + ":00"
    timestamp_list = new_written_time.split(' ')
    if (timestamp_list[1] == "오후"):
        time_list = timestamp_list[2].split(":")
        if (int(time_list[0]) != 12):
            time_list[0] = str(int(time_list[0])+12)
        else:
            time_list[0] = str(int(time_list[0]))
        timestamp_list[2] = ":".join(time_list)
                    
    new_written_time = timestamp_list[0] + ' ' + timestamp_list[2]
    return new_written_time


def get_each_news(links, drama_id):
    hdr = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36', 'Content-Type': 'application/json; charset=utf-8'}
    # browser = webdriver.Chrome('./chromedriver')
    for link in links:
        print("===== Start to crawl ", link, " =====")
        url_hash = hashlib.sha256(link.encode()).hexdigest()
        if (cursor.execute("SELECT title FROM naver_news WHERE url_hash=%s", [url_hash]) != 0):
            print("Already crawled news")
            continue
        # browser.get(link)
        # source = browser.page_source
        
        
        try:
            signal.signal(signal.SIGALRM, TimeoutException.alarm_handler)
            signal.alarm(10)
            response = requests.get(link, params=hdr)
            signal.alarm(0)
        except TimeoutException.TimeoutException as e:
            print(e, link)
            continue

        source = response.text
        data = bs(source, 'html.parser')
        body = data.find('body')
        main = body.select_one('div#wrap > div#content > div.end_ct > div.end_ct_area')
            
        
        try:
            if (main != None):
                # print(link)
                title = main.select_one('h2.end_tit').get_text().strip()
                written_time = main.select_one('div.article_info > span.author > em').get_text()
                body_text = main.select_one('div.end_body_wrp > div#articeBody').get_text().strip()
                # recommends = int(main.select_one('div.end_btn > div.tomain.as_addinfo > div#toMainContainer > a > em.u_cnt._count').get_text())

                new_written_time = sql_datetime_form(written_time)
                news_tuple = (drama_id, url_hash, title, new_written_time, body_text)
                # news_tuple = (drama_id, url_hash, title, new_written_time, body_text, recommends)

                cursor.execute("INSERT INTO naver_news(id, url_hash, title, modified_time, body_text) values (%s, %s, %s, %s, %s)", news_tuple)
                # cursor.execute("INSERT INTO naver_news(id, url_hash, title, modified_time, body_text, recommends) values (%s, %s, %s, %s, %s, %s)", news_tuple)
            
            # else:
            #     main = body.select_one('div#wrap > table.container > tr > td.content > div#main_content')
            #     title = main.select_one('div.article_header > div.article_info > h3').get_text()
            #     written_time = main.select_one('div.article_header > div.article_info > div.sponsor > span').get_text()
            #     body_text = main.select_one('div#articleBody > div#articleBodyContents').get_text().strip()
            #     # recommends = int(main.select_one('div#articleBody > div.end_bnt > div.tomain > div > a > em.u_cnt._count').get_text())

            #     new_written_time = sql_datetime_form(written_time)
            #     news_tuple = (drama_id, url_hash, title, new_written_time, body_text, recommends)

            #     cursor.execute("INSERT INTO naver_news(id, url_hash, title, modified_time, body_text, recommends) values (%s, %s, %s, %s, %s, %s)", news_tuple)
        
        except Exception as e:
            print("EXCEPTION!!!")
            print(e)


if __name__ == "__main__":
    connect_to_db()
    ##### CRAWL NEWS OF ALL DRAMAS #####
    # cursor.execute("SELECT id, drama_name from drama_info order by drama_name desc")
    # drama_id_name_list = cursor.fetchall()
    ##### CRAWL ONLY SPECIFIC DRAMAS #####
    drama_id_name_list = [(13, '비밀의숲2')]

    for drama in drama_id_name_list:
        for i in range(0, 500):
            links = search_news(drama[1], drama[0], i*10+1)
            get_each_news(links, drama[0])
            connection.commit()

    unconnect_to_db()
