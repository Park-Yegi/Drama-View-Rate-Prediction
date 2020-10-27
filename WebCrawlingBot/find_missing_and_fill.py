from selenium import webdriver
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
import requests
import time
import csv

drama_link = open('../drama_link.csv', 'r', encoding='utf-8')
link_rdr = csv.reader(drama_link)
all_drama_file = open('../all_drama.csv', 'r', encoding='utf-8')
drama_rdr = csv.reader(all_drama_file)
pd_link = open('../pd_link.csv', 'r', encoding='utf-8')
pd_rdr = csv.reader(pd_link)
wr_link = open('../wr_link.csv', 'r', encoding='utf-8')
wr_rdr = csv.reader(wr_link)

pd_name_list = []
wr_name_list = []
pd_link_list = []
wr_link_list = []

for line in pd_rdr:
    pd_name_list.append(line[0].strip())
    pd_link_list.append(line[1].strip())

for line in wr_rdr:
    wr_name_list.append(line[0].strip())
    wr_link_list.append(line[1].strip())

# browser = webdriver.Chrome('./chromedriver')
hdr = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36', 'Content-Type': 'application/json; charset=utf-8'}

for drama in link_rdr:
    title = drama[0].strip()
    link = drama[1]

    try:
        response = requests.get(link, params=hdr)
        source = response.text
        data = bs(source, 'html.parser')
        body = data.find('body')

        tab_list = body.select('div#wrap > div#container > div#content > div#main_pack > div.cs_common_module > div.cm_top_wrap > div.sub_tap_area > div > div > ul > li')
        pd_wr_link = ''
        for tab in tab_list:
            if (tab.select_one('a').get_text().strip() == '기본정보'):
                pd_wr_link = 'https://search.naver.com/search.naver' + tab.select_one("a").attrs['href']
                break

        if pd_wr_link != '':
            response = requests.get(pd_wr_link, params=hdr)
            source = response.text
            data = bs(source, 'html.parser')
            body = data.find('body')

            pro_info_list = body.select('div#wrap > div#container > div#content > div#main_pack > div.cs_common_module > div.cm_content_wrap > div.cm_content_area > div.cm_pure_box > div.pro_info_box > dl.pro_info > div.info_group')
            pd_a_list = []
            wr_a_list = []
            for pro_info in pro_info_list:
                if pro_info.select_one('dt').get_text().strip() == '제작진':
                    pro_list = pro_info.select('dd > ul > li')
                    for pro in pro_list:
                        # if pro.select_one('span.info').get_text().strip() == '연출':
                        #     pd_a_list = pro.select('span.text > a')
                        if (pro.select_one('span.info').get_text().strip() == '극본' or pro.select_one('span.info').get_text().strip() == '작가'):
                            wr_a_list = pro.select('span.text > a')
                
            if len(pd_a_list) == 0:
                print(title, "wr_a_list 없음")
            # if len(pd_a_list) == 0:
            #     print(title, "pd_a_list 없음")

            for each_pd in pd_a_list:
                each_pd_name = each_pd.get_text().strip()
                each_pd_link = 'https://search.naver.com/search.naver'+ each_pd.attrs['href']
                if each_pd_link in wr_link_list:
                    continue
                sub_response = requests.get(each_pd_link, params=hdr)
                sub_source = sub_response.text
                sub_data = bs(sub_source, 'html.parser')
                sub_body = sub_data.find('body')
                each_pd_link = sub_body.select('div#wrap > div#container > div#content > div#main_pack > div#people_info_z > div.go_relate > a')[-1].attrs['href']

                print('{0},{1}'.format(each_pd_name,each_pd_link))
                # for each_wr in wr_a_list:
                #     each_wr_name = each_wr.get_text().strip()
                #     each_wr_link = 'https://search.naver.com/search.naver'+ each_wr.attrs['href']
                #     sub_response = requests.get(each_wr_link, params=hdr)
                #     sub_source = sub_response.text
                #     sub_data = bs(sub_source, 'html.parser')
                #     sub_body = sub_data.find('body')
                #     each_wr_link = sub_body.select('div#wrap > div#container > div#content > div#main_pack > div#people_info_z > div.go_relate > a')[-1].attrs['href']

    except Exception as e:
        print(title, e)

drama_link.close()
all_drama_file.close()
pd_link.close()
wr_link.close()