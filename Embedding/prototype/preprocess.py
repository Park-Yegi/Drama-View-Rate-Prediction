import pymysql
import re


EMAIL_PATTERN = re.compile('[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', re.UNICODE)
URL_PATTERN = re.compile("((ftp|http|https):\/\/)?(www.)?(?!.*(ftp|http|https|www.))[a-zA-Z0-9-]+(\.[a-zA-Z]+)+((\/)[\w#]+)*(\/\w+\?[a-zA-Z0-9_]+=\w+(&[a-zA-Z0-9_]+=\w+)*)?$", re.UNICODE)
BRACKET_PATTERN = re.compile("(\[.*\])")
MULTIPLE_SPACES = re.compile(' +', re.UNICODE)
EMPTY_PARENTHESIS = re.compile('\( *\)', re.UNICODE)


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

    for i, news in enumerate(cursor):
        news_str = news[0].decode('utf-8')
        print(news_str)

        news_str = re.sub(re.compile("\]"), ']\n', news_str)
        news_str = re.sub(BRACKET_PATTERN, ' ', news_str)
        news_str = re.sub(re.compile("☞.*"), ' ', news_str)
        news_str = re.sub(re.compile("▶.*"), ' ', news_str)
        news_str = re.sub(re.compile("\(?\/? ?사진(제공)? ?= ?tvN\)?( 제공)?"), ' ', news_str)
        news_str = re.sub(re.compile('([가-힣]{3,4} )?[가-힣]{3,4} ?(온라인)?(객원)?(인턴)?기자( =)?'), ' ', news_str)
        news_str = re.sub(re.compile("(사진=)?방송 ?화면 캡처"), ' ', news_str)
        news_str = re.sub(re.compile('기사제보 및 보도자료'), ' ', news_str)
        news_str = re.sub(EMAIL_PATTERN, ' ', news_str)
        news_str = re.sub(EMPTY_PARENTHESIS, ' ', news_str)
        news_str = re.sub(MULTIPLE_SPACES, ' ', news_str)
        news_str = news_str.strip()
        

        print(news_str)

        print('==========================================================')
        
    
    connection.close()