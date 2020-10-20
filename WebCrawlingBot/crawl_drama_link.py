from selenium import webdriver
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
import requests
import time
import csv

browser = webdriver.Chrome('./chromedriver')
url = 'https://search.naver.com/search.naver?where=nexearch&sm=tab_etc&query=%EB%B0%A9%EC%98%81%EC%A2%85%EB%A3%8C%ED%95%9C%EA%B5%AD%EB%93%9C%EB%9D%BC%EB%A7%88'
browser.get(url)
time.sleep(2)
link_file = open('../drama_link.csv', 'w', encoding='utf-8')
wr = csv.writer(link_file)

year_list = ['2006년', '2007년', '2008년', '2009년', '2010년', '2011년', '2012년', '2013년', '2014년', '2015년', '2016년', '2017년', '2018년', '2019년', '2020년']
year_list.reverse()
year_button = browser.find_element_by_xpath("//li[@data-key='year']")

for year in year_list:
    year_button.click()
    time.sleep(2)

    year_xpath = "//li[@data-text='" + year + "']"
    each_year_button = browser.find_element_by_xpath(year_xpath)
    each_year_button.click()
    time.sleep(2)

    source = browser.page_source
    data = bs(source, 'html.parser')
    body = data.find('body')

    page_number = int(body.find('span', {'class':'_total'}).get_text())
    

    for i in range(1, page_number+1):
        drama_list = body.find('div', {'id':'mflick'}).select('div > div > ul > li')
        
        for drama in drama_list:
            title = drama.select_one('strong').get_text()
            link = 'https://search.naver.com/search.naver' + drama.select_one('strong > a').attrs['href']
            # wr.writerow([title, link])
            print(title, link)

        if (i != page_number):
            next_button = browser.find_element_by_xpath("//a[@class='pg_next _next on']")
            next_button.click()
            time.sleep(2)
            source = browser.page_source
            data = bs(source, 'html.parser')
            body = data.find('body')


link_file.close()