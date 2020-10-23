from selenium import webdriver
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
import requests
import time
import csv

drama_link = open('../drama_link.csv', 'r', encoding='utf-8')
link_rdr = csv.reader(drama_link)
all_drama_file = open('../all_drama.csv', 'w', encoding='utf-8')
drama_wr = csv.writer(all_drama_file)
column_name = ['title', 'start_date', 'end_date', 'day', 'time', 'num_eps', 'channel', 'next_drama', 'overview', 'pd1', 'pd2', 'pd3', 'wr1', 'wr2', 'wr3', 'ac1', 'ac2', 'ac3', 'ac4', 'first_rate', 'avg_rate', 'rate_25', 'prev', 'prev_25']
drama_wr.writerow(column_name)
pd_link = open('../pd_link.csv', 'w', encoding='utf-8')
pd_wr = csv.writer(pd_link)
wr_link = open('../wr_link.csv', 'w', encoding='utf-8')
wr_wr = csv.writer(wr_link)
actor_link = open('../actor_link.csv', 'w', encoding='utf-8')
ac_wr = csv.writer(actor_link)

# browser = webdriver.Chrome('./chromedriver')
hdr = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36', 'Content-Type': 'application/json; charset=utf-8'}

for drama in link_rdr:
    title = drama[0].strip()
    link = drama[1]
    start_date = ''
    end_date = ''
    day = ''
    broad_time = ''
    num_eps = ''
    channel = ''
    next_drama = ''
    overview = ''
    pd1 = ''
    pd2 = ''
    pd3 = ''
    wr1 = ''
    wr2 = ''
    wr3 = ''
    ac1 = ''
    ac2 = ''
    ac3 = ''
    ac4 = ''

    try:
        response = requests.get(link, params=hdr)
        source = response.text
        data = bs(source, 'html.parser')
        body = data.find('body')

        # browser.get(link)
        # source = browser.page_source
        # data = bs(source, 'html.parser')
        # body = data.find('body')
        main = body.select('div#wrap > div#container > div#content > div#main_pack > div.cs_common_module > div.cm_content_wrap > div.cm_content_area > div.cm_info_box > div.detail_info > dl.info > div.info_group')            
                        
        for info in main:
            if (info.select_one("dt").get_text() == "편성"):
                try:
                    print(title)
                    channel = info.select_one('dd > a').get_text().lower()
                    # print(channel)
                    start_date = info.select_one('dd > span').get_text().split('~')[0].replace('.', '-')[:-2].strip()
                    # print(start_date)
                    end_date = info.select_one('dd > span').get_text().split('~')[1].replace('.', '-')[:-2].strip().split(' ')[0][:-1]
                    # print(end_date)
                    num_eps = info.select_one('dd > span > em').get_text().replace('부작', '')
                    # print(num_eps)
                except Exception as e:
                    print(title, e)

                try:
                    day = info.select('dd > span.text')[1].get_text().split(')')[0][1:]
                    # print(day)
                    broad_time = info.select('dd > span.text')[1].get_text().split(')')[1].strip()
                    # print(broad_time)
                except Exception as e:
                    print(title, e)

        next_drama_struct = body.select_one('div#wrap > div#container > div#content > div#main_pack > div.cs_common_module > div.cm_content_wrap > div.cm_content_area > div.cm_info_box > div.horizon_box_image > div.list_info > div.info_box > strong > a')
        if next_drama_struct != None:
            next_drama = next_drama_struct.get_text()
        # print(next_drama)

        tab_list = body.select('div#wrap > div#container > div#content > div#main_pack > div.cs_common_module > div.cm_top_wrap > div.sub_tap_area > div > div > ul > li')
        # tab_list = body.select('div#wrap > div#container > div#content > div#main_pack > div#cs_common_module')
        pd_wr_link = ''
        ac_link = ''
        for tab in tab_list:
            if (tab.select_one('a').get_text().strip() == '기본정보'):
                pd_wr_link = 'https://search.naver.com/search.naver' + tab.select_one("a").attrs['href']
            elif (tab.select_one('a').get_text().strip() == '등장인물'):
                ac_link = 'https://search.naver.com/search.naver' + tab.select_one("a").attrs['href']

        if pd_wr_link != '':
            response = requests.get(pd_wr_link, params=hdr)
            source = response.text
            data = bs(source, 'html.parser')
            body = data.find('body')

            overview = body.select_one('div#wrap > div#container > div#content > div#main_pack > div.cs_common_module > div.cm_content_wrap > div.cm_content_area > div.cm_pure_box > div.intro_box > p').get_text()
            pro_info_list = body.select('div#wrap > div#container > div#content > div#main_pack > div.cs_common_module > div.cm_content_wrap > div.cm_content_area > div.cm_pure_box > div.pro_info_box > dl.pro_info > div.info_group')
            pd_list = []
            pd_a_list = []
            wr_list = []
            wr_a_list = []
            for pro_info in pro_info_list:
                if pro_info.select_one('dt').get_text().strip() == '제작진':
                    pro_list = pro_info.select('dd > ul > li')
                    for pro in pro_list:
                        if pro.select_one('span.info').get_text().strip() == '연출':
                            pd_list = pro.select_one('span.text').get_text().strip().split(',')
                            pd_a_list = pro.select('span.text > a')
                        elif (pro.select_one('span.info').get_text().strip() == '극본' or pro.select_one('span.info').get_text().strip() == '작가'):
                            wr_list = pro.select_one('span.text').get_text().strip().split(',')
                            wr_a_list = pro.select('span.text > a')

            if len(pd_list) == 1:
                pd1 = pd_list[0].strip()
            elif len(pd_list) == 2:
                pd1 = pd_list[0].strip()
                pd2 = pd_list[1].strip()
            elif len(pd_list) >= 3:
                pd1 = pd_list[0].strip()
                pd2 = pd_list[1].strip()
                pd3 = pd_list[2].strip()
            # print(pd1, pd2, pd3)

            if len(wr_list) == 1:
                wr1 = wr_list[0].strip()
            elif len(wr_list) == 2:
                wr1 = wr_list[0].strip()
                wr2 = wr_list[1].strip()
            elif len(wr_list) >= 3:
                wr1 = wr_list[0].strip()
                wr2 = wr_list[1].strip()
                wr3 = wr_list[2].strip()
            # print(wr1, wr2, wr3)
            
            for each_pd in pd_a_list:
                each_pd_name = each_pd.get_text().strip()
                each_pd_link = 'https://search.naver.com/search.naver'+ each_pd.attrs['href']
                sub_response = requests.get(each_pd_link, params=hdr)
                sub_source = sub_response.text
                sub_data = bs(sub_source, 'html.parser')
                sub_body = sub_data.find('body')
                each_pd_link = sub_body.select('div#wrap > div#container > div#content > div#main_pack > div#people_info_z > div.go_relate > a')[-1].attrs['href']
                pd_wr.writerow([each_pd_name, each_pd_link])

            for each_wr in wr_a_list:
                each_wr_name = each_wr.get_text().strip()
                each_wr_link = 'https://search.naver.com/search.naver'+ each_wr.attrs['href']
                sub_response = requests.get(each_wr_link, params=hdr)
                sub_source = sub_response.text
                sub_data = bs(sub_source, 'html.parser')
                sub_body = sub_data.find('body')
                each_wr_link = sub_body.select('div#wrap > div#container > div#content > div#main_pack > div#people_info_z > div.go_relate > a')[-1].attrs['href']
                wr_wr.writerow([each_wr_name, each_wr_link])

        if ac_link != '':
            response = requests.get(ac_link, params=hdr)
            source = response.text
            data = bs(source, 'html.parser')
            body = data.find('body')

            actor_list = body.select('div#wrap > div#container > div#content > div#main_pack > div.cs_common_module > div.cm_content_wrap > div.cm_tab_info_box > div.list_image_info > ul > li')[:4]
            # print(actor_list)
            ac_num = 1
            for actor in actor_list:
                per_actor = actor.select_one('div > div.title_box > span.sub_text > a')
                try:
                    per_actor_name = per_actor.get_text().strip()
                    per_actor_link = 'https://search.naver.com/search.naver' + per_actor.attrs['href']
                except:
                    per_actor_name = actor.select_one('div > div.title_box > span.sub_text').get_text().strip()
                    per_actor_link = ''
                
                if ac_num == 1:
                    ac1 = per_actor_name
                elif ac_num == 2:
                    ac2 = per_actor_name
                elif ac_num == 3:
                    ac3 = per_actor_name
                elif ac_num == 4:
                    ac4 = per_actor_name
                ac_num += 1

                if per_actor_link != '':
                    # print(per_actor_link)
                    sub_response = requests.get(per_actor_link, params=hdr)
                    sub_source = sub_response.text
                    sub_data = bs(sub_source, 'html.parser')
                    sub_body = sub_data.find('body')
                    # print(per_actor_name)
                    # print(sub_body.select_one('div#wrap > div#container > div#content > div#main_pack'))
                    per_actor_link = sub_body.select('div#wrap > div#container > div#content > div#main_pack > div#people_info_z > div.go_relate > a')[-1].attrs['href']

                ac_wr.writerow([per_actor_name, per_actor_link])
            # print(ac1, ac2, ac3, ac4)


        drama_wr.writerow([title, start_date, end_date, day, broad_time, num_eps, channel, next_drama, overview, pd1, pd2, pd3, wr1, wr2, wr3, ac1, ac2, ac3, ac4])

    except Exception as e:
        print("Total exception so may not recorded", title, e)

drama_link.close()
all_drama_file.close()
pd_link.close()
wr_link.close()
actor_link.close()