from selenium import webdriver
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
import requests
import time
import csv


browser = webdriver.Chrome('./chromedriver')
url = 'https://people.search.naver.com/search.naver?where=nexearch&sm=tab_ppn&query=%EC%9D%B4%EB%B3%91%ED%97%8C&os=94766&ie=utf8&key=PeopleService'
browser.get(url)
source = browser.page_source
time.sleep(2)
data = bs(source, 'html.parser')
body = data.find('body')

person = body.select_one("div#fix_wrap > div#wrap > div#container > div#content_wrap > div#content > div.people_wrap > div.profile_wrap > div.profile_dsc > dl.who > dt.name").get_text().strip()

### award
all_award_list = []
record_list = body.select("div#fix_wrap > div#wrap > div#container > div#content_wrap > div#content > div.people_wrap > div.record_wrap > div.record")
for record_set in record_list:
    if (record_set.select_one('h3').get_text() == '수상내역'):
        award_list = record_set.select('dl > dd')
        award_year_list = record_set.select('dl > dt')
        for i in range(len(award_list)):
            all_award_list.append((award_list[i].get_text().strip(), award_year_list[i].get_text().strip()))

all_award_list.reverse()
print("Award")
for x in all_award_list:
    print(*x, sep=',')
    # print(*x, sep=',', end=',')
print('\n')


## drama
try:
    page_number = body.select_one("div#fix_wrap > div#wrap > div#container > div#content_wrap > div#content > div.people_wrap > div.workact_wrap > div.workact_dsc > div > div > div#pagination_76 > span.count").get_text()
    page_number = int(page_number.split('/')[-1])
except:
    page_number = 1
all_drama_list = []


hdr = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36', 'Content-Type': 'application/json; charset=utf-8'}
drama_list = body.select("div#fix_wrap > div#wrap > div#container > div#content_wrap > div#content > div.people_wrap > div.workact_wrap > div.workact_dsc > div > div.workact.type5 > ul#listUI_76 > li")

for i in range(1, page_number+1):
    for drama in drama_list:
        title_wrap = drama.select_one("span.tit_wrap")
        title = title_wrap.get_text()
        link = title_wrap.select_one("a").attrs['href']
        response = requests.get(link, params=hdr)
        sub_source = response.text
        sub_data = bs(sub_source, 'html.parser')
        sub_body = sub_data.find('body')

        if (sub_body.select_one('div#wrap > div#container > div#content > div#main_pack > div.cs_common_module > div.cm_top_wrap > div.title_area > div.sub_title > span.txt > a').get_text().strip() != '드라마'):
            continue

        # main = sub_body.select_one('div#wrap > div#container > div > div > div > div > div > div > div > dl')
        main = sub_body.select('div#wrap > div#container > div#content > div#main_pack > div.cs_common_module > div.cm_content_wrap > div.cm_content_area > div.cm_info_box > div.detail_info > dl.info > div.info_group')
        
        channel = None
        start_date = None
        max_view_rate = None
        for info in main:
            if (info.select_one("dt").get_text() == "편성"):
                channel = info.select_one('dd > a').get_text().lower()
                start_date = info.select_one('dd > span').get_text().split('~')[0].replace('.', '-')[:-2].strip()
            elif (info.select_one('dt').get_text() == '시청률'):
                max_view_rate = info.select_one('dd > em').get_text().replace('%', '')
        # print((title, channel, start_date, max_view_rate))
        all_drama_list.append((title, channel, start_date, max_view_rate))
        

    if (i != page_number):  
        # browser.find_element_by_class_name('bt_next').click()
        browser.find_element_by_id('pagination_76').find_element_by_class_name('bt_next').click()
        time.sleep(2)
        source = browser.page_source
        time.sleep(2)
        data = bs(source, 'html.parser')
        body = data.find('body')
        drama_list = body.select("div#fix_wrap > div#wrap > div#container > div#content_wrap > div#content > div.people_wrap > div.workact_wrap > div.workact_dsc > div > div.workact.type5 > ul#listUI_76 > li")

all_drama_list.reverse()

# print(person, end=',')
print("Drama")
for x in all_drama_list:
    print(*x, sep=',')
    # print(*x, sep=',', end=',')
print('\n')



## movie
try:
    page_number = body.select_one("div#fix_wrap > div#wrap > div#container > div#content_wrap > div#content > div.people_wrap > div.workact_wrap > div.workact_dsc > div > div.workact.type5 > div#pagination_78 > span.count").get_text()
    page_number = int(page_number.split('/')[-1])
except:
    page_number = 1
all_movie_list = []


movie_list = body.select("div#fix_wrap > div#wrap > div#container > div#content_wrap > div#content > div.people_wrap > div.workact_wrap > div.workact_dsc > div > div.workact.type5 > ul#listUI_78 > li")

if movie_list != None:
    for i in range(1, page_number+1):
        # print(drama_list)
        for movie in movie_list:
            title_wrap = movie.select_one("span.tit_wrap")
            title = title_wrap.get_text()
            link = title_wrap.select_one("a").attrs['href']
            status_list = movie.select("span.dsc_area > span.status_sub")
            role = status_list[0].get_text().split('-')[0].strip()
            year = status_list[1].get_text().strip()[:-1]

            all_movie_list.append((title, role, year))
            

        if (i != page_number):  
            browser.find_element_by_id('pagination_78').find_element_by_class_name('bt_next').click()
            time.sleep(2)
            source = browser.page_source
            time.sleep(2)
            data = bs(source, 'html.parser')
            body = data.find('body')
            movie_list = body.select("div#fix_wrap > div#wrap > div#container > div#content_wrap > div#content > div.people_wrap > div.workact_wrap > div.workact_dsc > div > div.workact.type5 > ul#listUI_78 > li")


all_movie_list.reverse()
# print(all_drama_list)

print("Movie")
# print(person, end=',')
for x in all_movie_list:
    print(*x, sep=',')
    # print(*x, sep=',', end=',')
print('\n')