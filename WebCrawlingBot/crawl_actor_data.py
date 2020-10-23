from selenium import webdriver
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
import requests
import time
import csv
import traceback


browser = webdriver.Chrome('./chromedriver')
url_file = open('../kbs_actor.csv', 'r', encoding='utf-8')
rdr = csv.reader(url_file)
award_file = open('../kbs_actor_award.csv', 'w', encoding='utf-8')
award_wr = csv.writer(award_file)
drama_file = open('../kbs_actor_drama.csv', 'w', encoding='utf-8')
drama_wr = csv.writer(drama_file)
movie_file = open('../kbs_actor_movie.csv', 'w', encoding='utf-8')
movie_wr = csv.writer(movie_file)

for line in rdr:
    actor_name = line[0]
    url = line[1]
    # print(actor_name)
    # print(url)

    try:
        browser.get(url)
        source = browser.page_source
        time.sleep(2)
        data = bs(source, 'html.parser')
        body = data.find('body')

        # person = body.select_one("div#fix_wrap > div#wrap > div#container > div#content_wrap > div#content > div.people_wrap > div.profile_wrap > div.profile_dsc > dl.who > dt.name").get_text().strip()

        ### award
        all_award_list = []
        record_list = body.select("div#fix_wrap > div#wrap > div#container > div#content_wrap > div#content > div.people_wrap > div.record_wrap > div.record")
        for record_set in record_list:
            if (record_set.select_one('h3').get_text() == '수상내역'):
                award_list = record_set.select('dl > dd')
                award_year_list = record_set.select('dl > dt')
                for i in range(len(award_list)):
                    all_award_list.append(award_list[i].get_text().strip())
                    all_award_list.append(award_year_list[i].get_text().strip())

        award_wr.writerow([actor_name] + all_award_list)

    except Exception as e:
        print(actor_name, e)
        print(traceback.format_exc())


        ## drama
    try:
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
                channel = None
                start_date = None
                max_view_rate = None
                role = None
                title_wrap = drama.select_one("span.tit_wrap")
                title = title_wrap.get_text()
                link = title_wrap.select_one("a").attrs['href']
                status_list = drama.select("span.dsc_area > span.status_sub")
                if ('(' in status_list[0].get_text()):
                    role = status_list[0].get_text().split('(')[1].replace(')','').strip()

                response = requests.get(link, params=hdr)
                sub_source = response.text
                sub_data = bs(sub_source, 'html.parser')
                sub_body = sub_data.find('body')

                try:
                    if (sub_body.select_one('div#wrap > div#container > div#content > div#main_pack > div > div > div.title_area > div.sub_title > span.txt > a').get_text().strip() != '드라마'):
                        continue
                except:
                    print(actor_name, title)
                    continue

                # main = sub_body.select_one('div#wrap > div#container > div > div > div > div > div > div > div > dl')
                main = sub_body.select('div#wrap > div#container > div#content > div#main_pack > div.cs_common_module > div.cm_content_wrap > div.cm_content_area > div.cm_info_box > div.detail_info > dl.info > div.info_group')
                
                
                for info in main:
                    if (info.select_one("dt").get_text() == "편성"):
                        channel = info.select_one('dd > a').get_text().lower()
                        start_date = info.select_one('dd > span').get_text().split('~')[0].replace('.', '-')[:-2].strip()
                    elif (info.select_one('dt').get_text() == '시청률'):
                        max_view_rate = info.select_one('dd > em').get_text().replace('%', '')
                # print((title, channel, start_date, max_view_rate))
                all_drama_list.append(title)
                all_drama_list.append(channel)
                all_drama_list.append(start_date)
                all_drama_list.append(max_view_rate)
                all_drama_list.append(role)
                

            if (i != page_number):  
                # browser.find_element_by_class_name('bt_next').click()
                browser.find_element_by_id('pagination_76').find_element_by_class_name('bt_next').click()
                time.sleep(2)
                source = browser.page_source
                time.sleep(2)
                data = bs(source, 'html.parser')
                body = data.find('body')
                drama_list = body.select("div#fix_wrap > div#wrap > div#container > div#content_wrap > div#content > div.people_wrap > div.workact_wrap > div.workact_dsc > div > div.workact.type5 > ul#listUI_76 > li")

    #     all_drama_list.reverse()

    #     # print(person, end=',')
    #     print("Drama")
        # for x in all_drama_list:
    #         print(*x, sep=',')
    #         # print(*x, sep=',', end=',')
    #     print('\n')
        drama_wr.writerow([actor_name] + all_drama_list)

    except Exception as e:
        print(actor_name, e)
        print(traceback.format_exc())



        ## movie
    try:
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

                    all_movie_list.append(title)
                    all_movie_list.append(year)
                    all_movie_list.append(role)
                    

                if (i != page_number):  
                    browser.find_element_by_id('pagination_78').find_element_by_class_name('bt_next').click()
                    time.sleep(2)
                    source = browser.page_source
                    time.sleep(2)
                    data = bs(source, 'html.parser')
                    body = data.find('body')
                    movie_list = body.select("div#fix_wrap > div#wrap > div#container > div#content_wrap > div#content > div.people_wrap > div.workact_wrap > div.workact_dsc > div > div.workact.type5 > ul#listUI_78 > li")


    #     all_movie_list.reverse()
    #     # print(all_drama_list)

    #     print("Movie")
    #     # print(person, end=',')
        # for x in all_movie_list:
    #         print(*x, sep=',')
    #         # print(*x, sep=',', end=',')
    #     print('\n')
        movie_wr.writerow([actor_name] + all_movie_list)

    except Exception as e:
        print(actor_name, e)
        print(traceback.format_exc())


url_file.close()
award_file.close()
drama_file.close()
movie_file.close()