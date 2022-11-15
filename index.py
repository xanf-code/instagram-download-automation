import configparser
import cloudinary
import cloudinary.api
import urllib.request
import requests
from pathlib import Path
import shutil
import time
from instagrapi import Client
import random
from requests.exceptions import ProxyError
from urllib3.exceptions import HTTPError
from instagrapi.exceptions import (
    ClientConnectionError,
    ClientForbiddenError,
    ClientLoginRequired,
    ClientThrottledError,
    GenericRequestError,
    PleaseWaitFewMinutes,
    RateLimitError,
    SentryBlock,
)
import datetime
currentTime = datetime.datetime.now()

# Hashtag List
hashtags = [
    "writingcommunity",
    "moonquotes",
    "lyricedits",
    "poetsdaily",
    "vibez",
    "relatabletweets",
    "relatablequote",
    "sadtweets",
    "aesthetic",
    "tumblrquotes",
    "instaquote",
    "bookquote",
    "aestheticquotes",
    "relatableteen",
    "relatabletextposts",
    "sadquotespage",
    "lifequotestagram",
    "moodquotes",
    "mood",
    "icanrelate",
    "selfcarelove",
    "loveyouself",
    "sassyquotes",
    "relatable",
    "loverelationship",
    "tumblr",
    "healing",
]

# Followers
followers = [
    "22034694471",
    "9294170459",
    "39801559480",
    "25355898574",
    "45370826080",
    "24850497158"
]

comments = ["Really nice.", "I like this.", "Nice.", "OMG.", "Great feed!", "Reminds me of something ...", "Exellent.", "Love it.", "😀😀😀",
            "😃😃😃", "😄😃😀", "😁😁😁", "😆😆😆", "😅😅😅", "😂😂😂", "😊😊😊", "😇😇😇", "🙂🙂🙂🙂🙂", "😎 😎 😎", "😍😍😍", "😳😳😳", "😱😱😱", "👀", "💪💪💪", "🤘 🤘 🤘", "👍👍👍"
            ]

# Setup cloudinary configuration
config = configparser.ConfigParser()
config.read('config.ini')

proxy = [
    '10235',
    '10236',
    '10237',
    '10238',
    '10239'
]

port = random.choice(proxy)

# Instagrapi config
cl = Client()
cl = Client(proxy='http://' + config['proxy']['username'] + ':' +
            config['proxy']['password'] + '@' + config['proxy']['ipv6'] + ':' + port)
try:
    cl.login(config['instagram']['insta_username'],
             config['instagram']['insta_password'])
except (ProxyError, HTTPError, GenericRequestError, ClientConnectionError):
    # Network level
    cl.set_proxy(next_proxy())
except (SentryBlock, RateLimitError, ClientThrottledError):
    # Instagram limit level
    cl.set_proxy(next_proxy())
except (ClientLoginRequired, PleaseWaitFewMinutes, ClientForbiddenError):
    # Logical level
    cl.set_proxy(next_proxy())

cloudinary.config(
    cloud_name=config['cloudinary']['cloud_name'],
    api_key=config['cloudinary']['api_key'],
    api_secret=config['cloudinary']['api_secret']
)


def getUrl():
    image_info = cloudinary.api.resource('next_post')
    return image_info['secure_url']


def downloadImage():
    pic_url = getUrl()
    with open('next_post.jpg', 'wb') as handle:
        response = requests.get(pic_url, stream=True)

        if not response.ok:
            print(response)

        for block in response.iter_content(1024):
            if not block:
                break

            handle.write(block)


def uploadImagetoInstagam():
    cl.photo_upload(path="next_post.jpg",
                    caption="""
                 Follow @3am_thoughts5 for more relatable quotes ✨🥀
.
.
.
.
.
.
.
.
.
.
.
.
#writingcommunity #moonquotes #lyricedits #poetsdaily #vibez #relatabletweets #relatablequote #sadtweets #aesthetic #tumblrquotes #instaquote #bookquote #aestheticquotes #relatableteen #relatabletextposts #sadquotespage #lifequotestagram #moodquotes #mood #icanrelate #selfcarelove #loveyouself #sassyquotes #relatable #loverelationship #tumblr #healing
                 """)


def likehashtags():
    like_hashtag = random.sample(hashtags, 3)
    for hashtag in like_hashtag:
        medias = cl.hashtag_medias_top(hashtag, amount=25)
    for media in medias:
        cl.media_like(media.id)
        time.sleep(5)


def userFollowers():
    for follower in followers:
        users = cl.user_followers(follower, amount=20)
    for user in users:
        cl.user_follow(user)
        time.sleep(5)


def commentOnMedia():
    like_hashtag = random.sample(hashtags, 3)
    for hashtag in like_hashtag:
        medias = cl.hashtag_medias_top(hashtag, amount=20)
    for media in medias:
        comment = random.choice(comments)
        cl.media_comment(media.id, comment)
        time.sleep(5)


def instagramEngagement():
    # Get Most recent posts by Hashtag
    if currentTime.hour >= 9 and currentTime.hour <= 12:
        likehashtags()
        print("Liking hashtags Successful")
    # Follow users of a particular user
    elif currentTime.hour >= 15 and currentTime.hour <= 17:
        userFollowers()
        print("Following users Successful")
    # Comment on posts
    elif currentTime.hour >= 18 and currentTime.hour <= 24:
        commentOnMedia()
        print("Commenting on posts Successful")


def main():
    downloadImage()
    print("--------Image Downloaded Successfully--------")
    uploadImagetoInstagam()
    print("--------Image Uploaded Successfully--------")
    instagramEngagement()
    print("--------Instagram Engagement Successful--------")
    cl.logout()
    print("--------Logged Out Successfully--------")


main()
