import csv
import requests
from bs4 import BeautifulSoup as bs

drama_link = open('../drama_link.csv', 'r', encoding='utf-8')
all_drama = open('../all_drama.csv', 'r', encoding='utf-8')
# link_rdr = csv.reader(drama_link)
all_drama_rdr = csv.reader(all_drama)

after = 0
hdr = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36', 'Content-Type': 'application/json; charset=utf-8'}

for line in all_drama_rdr:
    title = line[0]
    if title == '보스를 지켜라':
        after = 1
    if after == 0:
        continue
    
    next_drama = line[9]
    link = None

    # try:
    if next_drama == '':
        # link_rdr = csv.reader(drama_link)
        # print(title)
        link_rdr = csv.reader(drama_link)
        for link_line in link_rdr:
            if link_line[0].strip() == title:
                link = link_line[1]
                break
        # print(link)        
            
        response = requests.get(link, params=hdr)
        source = response.text
        data = bs(source, 'html.parser')
        body = data.find('body')
        tab_list = body.select('div#wrap > div#container > div#content > div#main_pack > div.cs_common_module > div.cm_top_wrap > div.sub_tap_area > div > div > ul > li')

        for tab in tab_list:
            if (tab.select_one('a').get_text().strip() == '기본정보'):
                pd_wr_link = 'https://search.naver.com/search.naver' + tab.select_one("a").attrs['href']


        if pd_wr_link != '':
            response = requests.get(pd_wr_link, params=hdr)
            source = response.text
            data = bs(source, 'html.parser')
            body = data.find('body')

            next_drama_struct = body.select_one('div#wrap > div#container > div#content > div#main_pack > div.cs_common_module > div.cm_content_wrap > div.cm_content_area > div.cm_info_box > div.horizon_box_image > div.list_info > div.info_box > strong > a')
            if next_drama_struct != None:
                print(title, next_drama_struct.get_text())

    # except Exception as e:
    #     print(title, e)

drama_link.close()
all_drama.close()