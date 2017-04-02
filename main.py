from __future__ import print_function
import httplib2, requests, bs4, os, re, shutil, io, uuid

from apiclient.http import MediaIoBaseDownload
from apiclient.http import MediaFileUpload
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from oauth2client.service_account import ServiceAccountCredentials


import web_scraper
import httpserver

#########################################
# scrape websites and download torrents #
#########################################

#create scraper object
scraper_object = web_scraper.scraper() 

#define variables
DOWNLOAD_FOLDER = 'DOWNLOADS/'
UPLOAD_FOLDER = DOWNLOAD_FOLDER

#creates clean directory to store torrents
try:
	shutil.rmtree(DOWNLOAD_FOLDER)
except OSError:
	pass
os.mkdir(DOWNLOAD_FOLDER)


# These distributions have easy static links for their latest torrent downloads

# Download Raspian from a static link
scraper_object.downloadfile('http://downloads.raspberrypi.org/raspbian_latest.torrent',DOWNLOAD_FOLDER)
scraper_object.downloadfile('http://downloads.raspberrypi.org/raspbian_lite_latest.torrent',DOWNLOAD_FOLDER)
#Download Debian from the "current" folder
scraper_object.scrape('http://cdimage.debian.org/debian-cd/current/amd64/bt-cd/','netinst','true',DOWNLOAD_FOLDER)
#download Arch from the "latest" folder
scraper_object.scrape('http://mirror.rackspace.com/archlinux/iso/latest/','torrent','true',DOWNLOAD_FOLDER)


# These distributions require us to scrape their website to find their latest torrent downloads

# Download Ubuntu
scraper_object.scrape('http://www.ubuntu.com/download/alternative-downloads',"download-torrent",'false',DOWNLOAD_FOLDER)
# Download Kali


######################################
# Start Web Server                   #
######################################

httpserver_object = httpserver.httpserver(DOWNLOAD_FOLDER)

