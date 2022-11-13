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

# Instagrapi config
cl = Client()
cl.login(config['instagram']['insta_username'],
         config['instagram']['insta_password'])

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
                 Follow @3.am.__.talks for more relatable quotes ✨🥀
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
    for hashtag in hashtags:
        medias = cl.hashtag_medias_top_a1(hashtag, amount=1)
    for media in medias:
        cl.media_like(media.id)
        time.sleep(5)

def userFollowers():
    for follower in followers:
        users = cl.user_followers_gql(follower, amount=3)
    for user in users:
        cl.user_follow(user)
        time.sleep(10)

def commentOnMedia():
    comment = random.choice(comments)
    for hashtag in hashtags:
        medias = cl.hashtag_medias_top_a1(hashtag, amount=1)
    for media in medias:
        cl.media_comment(media.id, comment)
        time.sleep(10)
            
def instagramEngagement():
    # Get Most recent posts by Hashtag
    likehashtags()
    print("Liking hashtags Successful")
    time.sleep(5)
    # Follow users of a particular user
    userFollowers()
    print("Following users Successful")
    time.sleep(5)
    # Comment on posts
    commentOnMedia()
    print("Commenting on posts Successful")
    time.sleep(5)

def main():
    downloadImage()
    print("--------Image Downloaded Successfully--------")
    uploadImagetoInstagam()
    print("--------Image Uploaded Successfully--------")
    instagramEngagement()
    print("--------Instagram Engagement Successful--------")


main()
