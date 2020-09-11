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


def search_article(drama_name, drama_id):
    links = []
    hdr = {'User-Agent': 'Mozilla/5.0'}
    url = 'https://section.blog.naver.com/Search/Post.nhn?pageNo=1&rangeType=ALL&orderBy=sim&keyword='+drama_name
    browser = webdriver.Chrome('./chromedriver')
    browser.get(url)
    # response = requests.get(url, params=hdr)
    source = browser.page_source
    # source = response.text
    data = bs(source, 'html.parser')
    body = data.find('body')
    a_tags = body.select('ui-view > div#wrap > main#container > div.layout_content > div#content > section.wrap_search_list > div.area_list_search > div.list_search_post > div.item.multi_pic > div.info_post > div.desc > a.desc_inner')
    for a_tag in a_tags:
        links.append(a_tag.attrs['href'])
    # print(links)
    return links


def get_each_article(links):
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
        if (main != None):
            url_hash = hashlib.sha256(link.encode()).hexdigest()
            title = main.select_one('div > div > div > div > div > p').get_text()
            written_timestamp = main.select_one('div > div > div > div > span.se_publishDate').get_text()
            body_text_list = main.select('div.se-main-container > div.se-component > div.se-component-content > div.se-section > div.se-module > p.se-text-paragraph')
            body_text = ""
            for text_piece in body_text_list:
                body_text = body_text + text_piece.get_text()

            print(title)
            print(written_timestamp)
            print(body_text)
        


if __name__ == "__main__":
    drama_name = "비밀의숲2"
    drama_id = connect_to_db(drama_name)
    links = search_article(drama_name, drama_id)
    get_each_article(links)
    unconnect_to_db()
