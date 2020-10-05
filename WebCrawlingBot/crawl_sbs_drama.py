from bs4 import BeautifulSoup as bs
from selenium import webdriver
from urllib.request import urlopen
import requests
import csv
import time


hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36', 'Referer':'https://www.sbs.co.kr/', 'Upgrade-Insecure-Requests':1}
url = 'https://www.sbs.co.kr/tv/drama'

# response = requests.get(url, params=hdr)
# source = response.text

links = []
browser = webdriver.Chrome('./chromedriver')
browser.get(url)
browser.find_element_by_id('sbs-sports-programList-tab-end').click()
time.sleep(3)

source = browser.page_source

data = bs(source, 'html.parser')
body = data.find('body')

# drama_list = body.select('div#app-section-front-pc > div > div#container')
drama_li_tags = body.select('div#app-section-front-pc > div#sbs-gnb-self > div#container > div#sbs-gnb-content > div#sbs-drama-container-self > div.dr_main_wrap > div.dr_main_w > div#sbs-drama-container-main > div#sbs-drama-mainContainer-self > div#sbs-drama-mainContainer-area-programList > div#sbs-section-programList-self > div.main_programtab_w > div#sbs-sports-programList-area-list-self > div.main_programtab_inner > ul.main_programtab_list > li')
drama_list = []
try:
    for tag in drama_li_tags:
        tag.span.decompose()
        drama_name = tag.select_one('div > a > div.mb_cont_w > div.mb_title').get_text()
        # print(drama_name)
        drama_link = tag.select_one('div > a').attrs['href']
        # print(drama_link)
        subtext_list = tag.select_one('div > a > div.mb_cont_w > div.mb_subtext').get_text().split('|')
        # print(subtext_list)
        drama_date = subtext_list[0].strip()
        # print(drama_date)
        drama_start = subtext_list[1].split('~')[0].strip()
        # print(drama_start)
        drama_element = (drama_name, drama_link, drama_date, drama_start)
        drama_list.append(drama_element)
except Exception as e:
    print(e)

print(drama_list[:5])

# with open('../sbs_mini.csv', 'w', encoding='utf-8') as f:
#     writer = csv.writer(f)
#     for row in view_rate_table:
#         broadcasting_date = row.select_one('td').get_text().replace(".", "-")
#         episode = int(row.select_one('td > a').get_text().split('회')[0])
#         view_rate = float(row.select('td')[2].get_text()[:-1])
#         writer.writerow(tuple([drama_name, episode, view_rate, broadcasting_date]))