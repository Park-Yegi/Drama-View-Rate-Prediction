import csv
from bs4 import BeautifulSoup as bs
import requests

all_drama = open('../all_drama.csv', 'r', encoding='utf-8')
drama_rdr = csv.reader(all_drama)
hdr = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36', 'Content-Type': 'application/json; charset=utf-8'}

drama_name = []
after = 0
for line in drama_rdr:
    if line[0] == '마이더스':
        after = 1
    if after == 0:
        continue
    drama_name.append(line[0].replace(' ', '_'))

for drama in drama_name:
    genre = ''
    broad_time = ''
    link = 'https://ko.wikipedia.org/wiki/' + drama

    try:
        response = requests.get(link, params=hdr)
        source = response.text
        data = bs(source, 'html.parser')
        body = data.find('body')

        info_list = body.select('div#content > div#bodyContent > div#mw-content-text > div.mw-parser-output > table > tbody > tr')

        for info in info_list:
            table_head = info.select_one('th')

            if table_head != None:
                table_head_text = table_head.get_text().strip()
                if info.select_one('th').get_text().strip() == '장르':
                    genre = info.select_one('td').get_text().strip()
                elif info.select_one('th').get_text().strip().replace(' ', '') == '방송시간':
                    broad_time = info.select_one('td').get_text().strip()

        print(drama, genre, broad_time)

    except Exception as e:
        print(drama, e)