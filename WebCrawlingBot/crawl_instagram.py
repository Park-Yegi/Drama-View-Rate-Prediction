import os
import sys
import time
import textwrap
import argparse
import re
import pymysql
import MySQLdb
from my_insta_scraper import InstagramScraper


def connect_to_db():
    global connection
    global cursor

    connection = MySQLdb.connect(
        user="scrapingman",
        passwd="myPassword-1",
        host="localhost",
        db="scrapingdata",
        charset="utf8")

    cursor=connection.cursor()


def unconnect_to_db():
    connection.commit()
    connection.close()




def main(drama_id_name_list):
    maximum = 1

    ### test code for single drama
    hashtags = ['비밀의숲2']
    args = argparse.Namespace(followings_output=None,latest_stamps=None, maximum=maximum,
                                media_types=['none'],retry_forever=False, tag=True, username=hashtags)

    args.usernames = InstagramScraper.parse_delimited_str(','.join(args.username))

    if args.media_types and len(args.media_types) == 1 and re.compile(r'[,;\s]+').findall(args.media_types[0]):
        args.media_types = InstagramScraper.parse_delimited_str(args.media_types[0])

    if args.retry_forever:
        global MAX_RETRIES
        MAX_RETRIES = sys.maxsize

    scraper = InstagramScraper(**vars(args))

    scraper.authenticate_as_guest()

    try:
        metadata = scraper.scrape_hashtag()
    except Exception as e:
        print(e)
        time.sleep(1)

    scraper.save_cookies()

    print(metadata)
    post = metadata[0]
    insta_id = post['shortcode']
    body_text = post['edge_media_to_caption']['edges'][0]['node']['text']
    comments = post['edge_media_to_comment']['count']
    likes = post['edge_liked_by']['count']
    modified_time = post['taken_at_timestamp']
    new_tuple = (modified_time, body_text, likes, comments, insta_id)
    print(new_tuple)

    # for each in drama_id_name_list:
    #     hashtags = [each[1]]
    #     # args = argparse.Namespace(comments=False, cookiejar=None, destination='./', filename=None, filter=None, 
    #     #                             followings_input=False, followings_output=None, include_location=False, interactive=False,
    #     #                             lastest=False, latest_stamps=None, location=False, login_pass=None, login_user=None, maximum=maximum,
    #     #                             media_metadata=False, media_types=media_types, no_check_certificate=False, profile_metadata=False,
    #     #                             proxies={}, quiet=False, retain_username=False, retry_forever=False, search_location=False, tag=True, template='{urlname}', username=hashtags, verbose=0)

    #     args = argparse.Namespace(followings_output=None,latest_stamps=None, maximum=maximum,
    #                                 media_types=['none'],retry_forever=False, tag=True, username=hashtags)

    #     args.usernames = InstagramScraper.parse_delimited_str(','.join(args.username))

    #     if args.media_types and len(args.media_types) == 1 and re.compile(r'[,;\s]+').findall(args.media_types[0]):
    #         args.media_types = InstagramScraper.parse_delimited_str(args.media_types[0])

    #     if args.retry_forever:
    #         global MAX_RETRIES
    #         MAX_RETRIES = sys.maxsize

    #     scraper = InstagramScraper(**vars(args))

    #     scraper.authenticate_as_guest()

    #     try:
    #         metadata = scraper.scrape_hashtag()
    #     except Exception as e:
    #         print(e)
    #         time.sleep(1)

    #     scraper.save_cookies()

    #     drama_id = each[0]
    #     for post in metadata:
    #         insta_id = post['id']
    #         body_text = post['edge_media_to_caption']['edges'][0]['node']['text']
    #         comments = post['edge_media_to_comment']['count']
    #         likes = post['edge_liked_by']['count']
    #         modified_time = post['taken_at_timestamp']
    #         new_tuple = (drama_id, modified_time, body_text, likes, comments, insta_id)
    #         print(new_tuple)
    #         try:
    #             cursor.execute("INSERT INTO instagram(id, modified_time, body_text, likes, comments, insta_id) values (%s, %s, %s, %s, %s, %s)", new_tuple)
    #         except Exception as e:
    #             print(e)

    #     connection.commit()


if __name__ == '__main__':
    connect_to_db()
    cursor.execute("SELECT id, drama_name from drama_info order by drama_name desc")
    drama_id_name_list = cursor.fetchall()
    main(drama_id_name_list)
    unconnect_to_db()