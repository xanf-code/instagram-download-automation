import configparser
import cloudinary
import cloudinary.api
import urllib.request
import requests

# Setup cloudinary configuration
config = configparser.ConfigParser()
config.read('config.ini')

cloudinary.config(
    cloud_name = config['cloudinary']['cloud_name'],
    api_key = config['cloudinary']['api_key'],
    api_secret = config['cloudinary']['api_secret']
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

def main():
    downloadImage()
    print("Image Downloaded Successfully")
    
main()