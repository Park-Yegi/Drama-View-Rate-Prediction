import pymysql
import re
from konlpy.tag import Mecab


EMAIL_PATTERN = re.compile('(\/ )?[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', re.UNICODE)
NAME_EMAIL_PATTERN = re.compile('[가-힣]{3,4} \(?[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+\)?', re.UNICODE)
URL_PATTERN = re.compile("((ftp|http|https):\/\/)?(www.)?(?!.*(ftp|http|https|www.))[a-zA-Z0-9-]+(\.[a-zA-Z]+)+((\/)[\w#]+)*(\/\w+\?[a-zA-Z0-9_]+=\w+(&[a-zA-Z0-9_]+=\w+)*)?$", re.UNICODE)
BRACKET_PATTERN = re.compile("(\[.*\])")
MULTIPLE_SPACES = re.compile(' +', re.UNICODE)
EMPTY_PARENTHESIS = re.compile('\( *\)', re.UNICODE)
NEW_LINE = re.compile("\n", re.UNICODE)
DATE_PATTERN = re.compile('[0-9]{4}\.[0-9]{2}\.[0-9]{2}\.')

def connect_to_db():
    global connection
    global cursor

    connection = pymysql.connect(
        user="scrapingman",
        passwd="myPassword-1",
        host="localhost",
        db="scrapingdata",
        charset="utf8")

    cursor = connection.cursor()


if __name__ == "__main__":
    connect_to_db()
    cursor.execute("SELECT body_text from naver_news where id=13")
    # cursor.execute("SELECT body_text from naver_news where news_id=940")

    corpus_fname = './corpus_mecab.txt'
    corpus_file = open(corpus_fname, 'w')

    for i, news in enumerate(cursor):
        news_str = news[0].decode('utf-8')
        # print(news_str)

        news_str = re.sub(re.compile("마이데일리\(www\.mydaily\.co\.kr\)\. 무단전재\&재배포 금지", re.UNICODE), ' ', news_str)
        news_str = re.sub(re.compile("여러분의 다양한 의견 달아주세요", re.UNICODE), ' ', news_str)
        
        news_str = re.sub(re.compile("▶.*", re.UNICODE), ' ', news_str)
        news_str = re.sub(re.compile("☞.*", re.UNICODE), ' ', news_str)
        news_str = re.sub(re.compile("\]", re.UNICODE), ']\n', news_str)
        news_str = re.sub(BRACKET_PATTERN, ' ', news_str)

        news_str = re.sub(re.compile("[가-힣]{3} ?(온라인|객원|인턴) ?기자", re.UNICODE), ' ', news_str)
        news_str = re.sub(re.compile("\/[가-힣]{3} ?기자", re.UNICODE), ' ', news_str)
        

        news_str = re.sub(re.compile("무단전재 & 재배포 금지", re.UNICODE), ' ', news_str)
        news_str = re.sub(re.compile("Sonny 프리시즌 활약상 ", re.UNICODE), ' ', news_str)
        news_str = re.sub(re.compile("\(주\)데일리안 \- 무단전재\, 변형\, 무단배포 금지", re.UNICODE), ' ', news_str)
        news_str = re.sub(re.compile('기사제보 및 보도자료', re.UNICODE), ' ', news_str)
        news_str = re.sub(NAME_EMAIL_PATTERN, ' ', news_str)
        news_str = re.sub(EMAIL_PATTERN, ' ', news_str)
        news_str = re.sub(re.compile("YTN Star", re.UNICODE), ' ', news_str)
        news_str = re.sub(re.compile("© 뉴스1\(서울\=뉴스1\)", re.UNICODE), ' ', news_str)
        news_str = re.sub(re.compile("매경닷컴 MK스포츠 뉴스팀", re.UNICODE), ' ', news_str)
        news_str = re.sub(re.compile("iMBC [가-힣]{3,4}", re.UNICODE), ' ', news_str)
        news_str = re.sub(re.compile("뉴스엔.*뉴스엔.", re.UNICODE), ' ', news_str)

        news_str = re.sub(re.compile("[가-힣]{3,4} 한경닷컴 연예·이슈팀 기자", re.UNICODE), ' ', news_str)
        news_str = re.sub(re.compile("글 : [가-힣]{3}\(칼럼니스트\)", re.UNICODE), ' ', news_str)
        
        
        news_str = re.sub(re.compile("(사진=)?방송 ?화면 캡처", re.UNICODE), ' ', news_str)
        news_str = re.sub(re.compile('\/?([가-힣]{3,6} ?)?=?[가-힣]{3,4} ?(온라인)?(객원)?(인턴)?기자( =)?', re.UNICODE), ' ', news_str)


        # news_str = re.sub(re.compile("", re.UNICODE), ' ', news_str)
        # news_str = re.sub(re.compile("", re.UNICODE), ' ', news_str)
        
        news_str = re.sub(re.compile("사진제공｜OCN·tvN", re.UNICODE), ' ', news_str)
        news_str = re.sub(re.compile("사진제공 (= )?tvN", re.UNICODE), ' ', news_str)
        news_str = re.sub(re.compile("방송화면", re.UNICODE), ' ', news_str)
        news_str = re.sub(re.compile("\(사진= *.{3,14} ?제공\)", re.UNICODE), ' ', news_str)
        news_str = re.sub(re.compile("\(사진= *.{3,12} ?캡처\)", re.UNICODE), ' ', news_str)
        news_str = re.sub(re.compile("\(?\/? ?사진(제공)? ?= *.{3}\)? ?(제공)?(캡처)?\)?", re.UNICODE), ' ', news_str)
        news_str = re.sub(re.compile("스틸컷\.?", re.UNICODE), ' ', news_str)
        news_str = re.sub(re.compile("tvN 제공\.?", re.UNICODE), ' ', news_str)
        news_str = re.sub(re.compile("제공|tvN", re.UNICODE), ' ', news_str)
        news_str = re.sub(re.compile("방송캡쳐", re.UNICODE), ' ', news_str)
        

        news_str = re.sub(re.compile("bogo109@", re.UNICODE), ' ', news_str)
        news_str = re.sub(re.compile("ⓒtvN", re.UNICODE), ' ', news_str)
        news_str = re.sub(re.compile("ⓒ", re.UNICODE), '', news_str)
        news_str = re.sub(re.compile("\|", re.UNICODE), '', news_str)
        news_str = re.sub(re.compile("\ㅣ", re.UNICODE), '', news_str)
        news_str = re.sub(re.compile("﻿", re.UNICODE), '', news_str)
        news_str = re.sub(re.compile("▲", re.UNICODE), '', news_str)
        news_str = re.sub(re.compile('\-'), '', news_str)
        news_str = re.sub(re.compile('\>'), '', news_str)
        news_str = re.sub(re.compile('\<'), '', news_str)
        news_str = re.sub(re.compile('■'), '', news_str)
        news_str = re.sub(re.compile('◆'), '', news_str)
        news_str = re.sub(re.compile("'"), '', news_str)
        news_str = re.sub(re.compile('‘'), '', news_str)
        news_str = re.sub(re.compile('’'), '', news_str)
        news_str = re.sub(DATE_PATTERN, ' ', news_str)
        # news_str = re.sub(re.compile("\.", re.UNICODE), '.\n', news_str)
        news_str = re.sub(EMPTY_PARENTHESIS, ' ', news_str)
        news_str = re.sub(NEW_LINE, ' ', news_str)
        news_str = re.sub(MULTIPLE_SPACES, '', news_str)
        news_str = re.sub(re.compile('\\xa0'), '', news_str)
        news_str = re.sub(re.compile("저작권자 SPOTV NEWS 무단전재 및 재배포 금지"), ' ', news_str)


        news_str = news_str.strip()
        # print(news_str)

        tokenizer = Mecab()
        tokens = tokenizer.morphs(news_str)
        corpus_file.writelines("%s " % token for token in tokens)
        corpus_file.write("\n")


        ####### JUST ONE NEWS FOR TEST ########
        # break
        #######################################
        
    
    connection.close()
    corpus_file.close()