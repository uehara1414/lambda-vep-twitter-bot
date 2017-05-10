import os
import sys

sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'vendor'))  # noqa

import gspread
import tweepy
from oauth2client.service_account import ServiceAccountCredentials


DEBUG = os.getenv('DEBUG', False)


def get_worksheet():
    scope = ['https://spreadsheets.google.com/feeds']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)

    sheet = client.open("lambda-bot-log")
    for worksheet in sheet.worksheets():
        if worksheet.id == 'od6':
            return worksheet


def get_uehara_api() -> tweepy.API:
    """メンションを監視する自分のアカウントの Tweepy API Object を返します
    :return: メンションを監視する自分のアカウントの Tweepy API Object
    """
    CONSUMER_KEY = os.environ["UEHARA_CONSUMER_KEY"]
    CONSUMER_SECRET = os.environ["UEHARA_CONSUMER_SECRET"]

    ACCESS_TOKEN = os.environ["UEHARA_ACCESS_TOKEN"]
    ACCESS_SECRET = os.environ["UEHARA_ACCESS_SECRET"]

    return get_api(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET)


def get_tsugumi_api() -> tweepy.API:
    """引用リツイートをするアカウントの Tweepy API Object を返します
    :return: 引用リツイートをするアカウントの Tweepy API Object
    """
    CONSUMER_KEY = os.environ["TSUGUMI_CONSUMER_KEY"]
    CONSUMER_SECRET = os.environ["TSUGUMI_CONSUMER_SECRET"]

    ACCESS_TOKEN = os.environ["TSUGUMI_ACCESS_TOKEN"]
    ACCESS_SECRET = os.environ["TSUGUMI_ACCESS_SECRET"]

    return get_api(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET)


def get_api(consumer_key: str, consumer_secret: str, access_token: str, access_secret: str):
    """API, ゲットだぜ！
    """
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    return tweepy.API(auth)


def is_already_retweeted_before(tweet_id: str) -> bool:
    worksheet = get_worksheet()
    tweeted_ids = [row[0] for row in worksheet.get_all_values()]
    return tweet_id in tweeted_ids


def record_as_tweeted(tweet):
    worksheet = get_worksheet()
    worksheet.append_row([tweet.id_str, tweet.author.screen_name, tweet.text, tweet.created_at])


def construct_text_Python_is_good(display_name, tweet_id):
    content = "https://twitter.com/{}/status/{}".format(display_name, tweet_id)
    content += "\n@{} Pythonはいいぞ!".format(display_name)
    return content


def get_new_mention_with_VEP() -> list:
    api = get_uehara_api()
    l = api.mentions_timeline()

    targets = []
    for x in l:
        if 'VEP' in x.text.upper() and not is_already_retweeted_before(x.id_str):
            targets.append(x)
    return targets


def retweet_with_Python_is_good(display_name, tweet_id):
    api = get_tsugumi_api()
    content = construct_text_Python_is_good(display_name, tweet_id)
    api.update_status(content)


def lambda_handler(event, context):
    targets = get_new_mention_with_VEP()
    for x in targets:
        if DEBUG:
            content = construct_text_Python_is_good(x.author.screen_name, x.id_str)
            print("dry retweet", content)
        else:
            retweet_with_Python_is_good(x.author.screen_name, x.id_str)
            record_as_tweeted(x)


if __name__ == '__main__':
    lambda_handler(None, None)
