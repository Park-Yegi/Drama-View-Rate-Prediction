import os
import sys
import time
import textwrap
import argparse
import re
from my_insta_scraper import InstagramScraper


def main():
    maximum = 5
    media_types = ['image', 'video', 'story-image', 'story-video'],
    hashtags=['비밀의숲2', '악의꽃', '청춘기록']

    # args = argparse.Namespace(comments=False, cookiejar=None, destination='./', filename=None, filter=None, 
    #                             followings_input=False, followings_output=None, include_location=False, interactive=False,
    #                             lastest=False, latest_stamps=None, location=False, login_pass=None, login_user=None, maximum=maximum,
    #                             media_metadata=False, media_types=media_types, no_check_certificate=False, profile_metadata=False,
    #                             proxies={}, quiet=False, retain_username=False, retry_forever=False, search_location=False, tag=True, template='{urlname}', username=hashtags, verbose=0)

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


if __name__ == '__main__':
    main()