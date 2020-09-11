from selenium import webdriver
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
import requests
import MySQLdb

def crawl_view_rate(drama_name, drama_id):
    hdr = {'User-Agent': 'Mozilla/5.0'}
    url = 'https://search.daum.net/search?w=tv&q='+drama_name +'시청률'
    # browser = webdriver.Chrome('./chromedriver')
    # browser.get(url)
    # source = browser.page_source
    response = requests.get(url, params=hdr)
    source = response.text
    data = bs(source, 'html.parser')
    body = data.find('body')
    view_rate_table = body.select('div.detail_wrap > div#tvpColl > div.coll_cont > div.mg_cont > div#tab_content > div#tabCont > div#tv_rating > div.wrap_rank > table.tbl_rank > tbody > tr')
    
    for row in view_rate_table:
        broadcasting_date = row.select_one('td').get_text()
        episode = row.select_one('td.center > a').get_text()
        view_rate = row.select('td')[2].get_text()
        error = save_to_db([drama_id, episode, view_rate,broadcasting_date])
        if (error != None):
            break


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


def save_to_db(drama_tuple):
    # print(drama_tuple[1][:-2])
    # print(drama_tuple[2][:-1])
    # print(drama_tuple[3])
    drama_tuple[1] = int(drama_tuple[1][:-2])
    drama_tuple[2] = float(drama_tuple[2][:-1])
    drama_tuple[3] = drama_tuple[3].replace(".", "-")
    drama_tuple = tuple(drama_tuple)
    # print(drama_tuple)
    try:
        cursor.execute("INSERT INTO view_rate values (%s, %s, %s, %s)", drama_tuple)
    except MySQLdb._exceptions.IntegrityError as e:
        print("Primary key (" + str(drama_tuple[0]) + ", " + str(drama_tuple[1]) + ") is already in the database")
        return e


if __name__ == "__main__":
    drama_name = "비밀의숲2"
    drama_id = connect_to_db(drama_name)
    crawl_view_rate(drama_name, drama_id)
    unconnect_to_db()

    