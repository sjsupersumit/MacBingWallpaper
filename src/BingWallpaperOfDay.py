from random import randint
import logging
import sys
import requests
import json
import datetime
import subprocess
import os
from appscript import *


BING_URL = "http://www.bing.com"
BASE_DIR = "/Users/sumit.jha/Desktop/wallpaper"


def main():
    file_path = download_image()
    set_wallpaper(file_path)


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


def set_wallpaper(file_path):
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