# MacBingWallpaper

Change the wallpaper of your mac with images from Flickr based on certain tags. Additionally you can also alter the tags in settings file to suit to your interests.

Obtain your Api key from flickr and put it in settings.conf file. After that just run this Script as

python path/MacBingWallpaper/src/BingWallpaperOfDay.py

and it will change the wallpaper of your mac on osx.

You can also Schedule a cron job to change the wallpaper automatically each day or after some hours like

0 */4 * * * /usr/bin/python path/MacBingWallpaper/src/BingWallpaperOfDay.py

it will executes this script in every 4 hours.




