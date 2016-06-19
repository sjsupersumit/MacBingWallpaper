from random import randint
import logging
import sys
import requests
import json
import datetime
import subprocess
import os
import ConfigParser
from appscript import *


BING_URL= "http://www.bing.com"
BASE_DIR= "/Users/sumit.jha/Desktop/wallpaper"

def main():
    try:
        file_path = download_from_flickr()
        set_wallpaper(file_path)
    except Exception as e:
        print "Exception occured..." + str(e)



def download_image():
    index = randint(1, 15)
    offset = randint(1, 100)
    base_url = "http://www.bing.com/HPImageArchive.aspx"
    params = {
        'format': 'js',
        'idx': index,
        'n': offset,
        'mkt': 'en-US'
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = json.loads(response.content)
        image_url = BING_URL + data['images'][0]['url']
        print image_url
        response = requests.get(image_url)
        if response.status_code == 200:
            date_time_str = datetime.datetime.now().strftime("%I:%M%p%s on %B %d, %Y")
            if not os.path.exists(BASE_DIR) :
                os.makedirs(BASE_DIR)
            file_path = "/Users/sumit.jha/Desktop/wallpaper/wp" + date_time_str + ".jpg"
            f = open(file_path, 'wb')
            f.write(response.content)
            f.close()
            return file_path


def download_from_flickr():
    flickr_api_base_url = "https://api.flickr.com/services/rest/"
    config = ConfigParser.ConfigParser()
    dir = os.path.dirname(__file__)
    config.read(os.path.join(dir, 'settings.conf'))
    key = config.get('Flickr', 'API_KEY')
    params = {
        'api_key': key,
        'tags': ['bliss','outdoors', 'beautiful', 'wallpaper', 'hd', 'motivation', 'inspiration', 'exotic'],
        'tag_mode': 'any',
        'safe_search': '2',
        'content_type': '1',
        'format':'json',
        'method': 'flickr.photos.search',
        'nojsoncallback': '1'
    }
    response = requests.get(flickr_api_base_url, params)
    if response.status_code == 200:
        data = json.loads(response.content)
        total =  int(data['photos']['total'])
        if total > 100:
            total = 100
        image_no = randint(0,total)
        photo_detail = data['photos']['photo'][image_no]
        photo_id = str(photo_detail['id'])
        owner = photo_detail['owner']
        farm_id = str(photo_detail['farm'])
        server_id = str(photo_detail['server'])
        secret = str(photo_detail['secret'])
        flickr_photo_url = "https://farm" + farm_id + ".staticflickr.com/" + server_id + "/" + photo_id +"_" + secret + "_h.jpg"
        response = requests.get(flickr_photo_url)
        if response.status_code == 200:
            if not os.path.exists(BASE_DIR) :
                os.makedirs(BASE_DIR)
            file_path = BASE_DIR + "/" + photo_id + ".jpg"
            f = open(file_path, 'wb')
            f.write(response.content)
            f.close()
            return file_path

def set_wallpaper(file_path):

    if file_path is None:
        return
    SCRIPT = """/usr/bin/osascript<<END
                ignoring application responses
                tell application "Finder"
                set desktop picture to POSIX file "%s"
                end tell
                END"""

    subprocess.Popen(SCRIPT%file_path, shell=True)
    f = file_path
    """Changes on All desktops """
    se = app('System Events')
    desktops = se.desktops.display_name.get()
    for d in desktops:
        desk = se.desktops[its.display_name == d]
        desk.picture.set(mactypes.File(f))


if __name__ == '__main__':
    main()