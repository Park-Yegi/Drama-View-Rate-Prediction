from selenium import webdriver
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
import requests
import hashlib
import MySQLdb
import time

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


def search_article(drama_name, drama_id, pageNo):
    links = []
    # hdr = {'User-Agent': 'Mozilla/5.0'}
    browser = webdriver.Chrome('./chromedriver')

    url = 'https://section.blog.naver.com/Search/Post.nhn?pageNo=' + str(pageNo) +'&rangeType=ALL&orderBy=sim&keyword='+drama_name
    browser.get(url)
    # response = requests.get(url, params=hdr)
    source = browser.page_source
    # source = response.text
    data = bs(source, 'html.parser')
    body = data.find('body')
    a_tags = body.select('ui-view > div#wrap > main#container > div.layout_content > div#content > section.wrap_search_list > div.area_list_search > div.list_search_post > div.item.multi_pic > div.info_post > div.desc > a.desc_inner')
    for a_tag in a_tags:
        links.append(a_tag.attrs['href'])

    return links


def get_each_article(links, drama_id):
    browser = webdriver.Chrome('./chromedriver')
    for link in links:
        browser.get(link)
        browser.switch_to.frame('mainFrame')
        # hdr = {'User-Agent': 'Mozilla/5.0'}
        # response = requests.get(link, params=hdr)
        source = browser.page_source
        # source = response.text
        data = bs(source, 'html.parser')
        body = data.find('body')
        main = body.select_one('div#head-skin > div#body > div#whole-border > div#whole-body > div#wrapper > div#twocols > div#content-area > div > div > div > div > table > tbody > tr > td.bcc > div > div.se-viewer')
        footer = body.select_one('div#head-skin > div#body > div#whole-border > div#whole-body > div#wrapper > div#twocols > div#content-area > div > div > div > div > table > tbody > tr > td.bcc > div > div.wrap_postcomment')
        # footer = body.select_one('div#head-skin > div#body > div#whole-border > div#whole-body > div#wrapper > div#twocols > div#content-area > div > div > div > div > table > tbody > tr > td.bcc > div.post-btn > div.wrap_postcomment')
        if (main == None):
            main = body.select_one('div#head-skin > div#body > div#whole-border > div#whole-body > div#wrapper > div#twocols > div#content-area > div > div > div > div > table.post-body > tbody > tr > td.bcc > div > div.view > div.se-viewer')
        
        if (main != None):
            url_hash = hashlib.sha256(link.encode()).hexdigest()
            title = main.select_one('div > div > div > div > div > p').get_text()
            written_timestamp = main.select_one('div > div > div > div > span.se_publishDate').get_text()
            body_text_list = main.select('div.se-main-container > div.se-component > div.se-component-content > div.se-section > div.se-module > p.se-text-paragraph')
            body_text = ""
            for text_piece in body_text_list:
                body_text = body_text + text_piece.get_text()
            # likes = footer.select('div.area_sympathy > a > div > span > em')[1].get_text()
            # comments = int(footer.select_one('div.area_comment > a > em').get_text().strip())

            # print(title)
            # print(written_timestamp)
            # print(body_text)
            # print(likes)
            # print(comments)

            if (written_timestamp[-1] == '전'):
                time_list = written_timestamp.split('시')
                time_before = int(time_list[0])
                now = time.localtime()
                if (time_before < now.tm_hour):
                    written_time = "%04d-%02d-%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour-time_before, now.tm_min, now.tm_sec)
                else:
                    if (now.tm_mday != 1):
                        written_time = "%04d-%02d-%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday-1, now.tm_hour-time_before+24, now.tm_min, now.tm_sec)
                    else:
                        if (now.tm_mon != 1):
                            written_time = "%04d-%02d-%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
                        else:
                            written_time = "%04d-%02d-%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
            else: 
                written_time = written_timestamp.replace('. ', '-', 2).replace('.', "") + ":00"

                
            # news_tuple = (drama_id, url_hash, title, written_time, body_text, likes, comments)
            news_tuple = (drama_id, url_hash, title, written_time, body_text)
            # print(drama_id)
            # print(url_hash)
            # print(title)
            # print(written_time)
            # print(body_text)
            # print(likes)
            # print(comments)

            try:
                # cursor.execute("INSERT INTO naver_blog(id, url_hash, title, modified_time, body_text, likes, comments) values (%s, %s, %s, %s, %s, %s, %s)", news_tuple)
                cursor.execute("INSERT INTO naver_blog(id, url_hash, title, modified_time, body_text) values (%s, %s, %s, %s, %s)", news_tuple)
            except Exception as e:
                print(e)
            
        else:
            print("Cannot Crawl this naver blog: %s", link)
            
        


if __name__ == "__main__":
    drama_name = "비밀의숲2"
    drama_id = connect_to_db(drama_name)

    for pageNo in range(0, 10):
        links = search_article(drama_name, drama_id, pageNo)
        get_each_article(links, drama_id)

    unconnect_to_db()
