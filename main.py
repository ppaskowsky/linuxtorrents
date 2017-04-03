from __future__ import print_function
import httplib2, requests, bs4, os, re, shutil, io, uuid, datetime, urlparse

from apiclient.http import MediaIoBaseDownload
from apiclient.http import MediaFileUpload
from apiclient import discovery

from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from oauth2client.service_account import ServiceAccountCredentials

from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

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


#########################################
# Write Dyno Startup Time to Postgres   #
#########################################

#pull postgres url from heroku environment variable
urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(os.environ["DATABASE_URL"])

db_url = (url.netloc)
database = (url.path)
final_url = ('postgresql://'+db_url+database)
print (final_url)

#Create a DBAPI connection
engine = create_engine(final_url)

#Declare an instance of the Base class for mapping tables
Base = declarative_base()

#Map a table to a class by inheriting base class
class Logs(Base):
    __tablename__ = "Logs"

    Id = Column(Integer, primary_key=True)
    AccessTime = Column(DateTime)

#create all tables if they do not exist
Base.metadata.create_all(engine)

#create session to DB        
Session = sessionmaker(bind=engine)
session = Session()

#execute commands via sqlalchemy orm
command1 = Logs(AccessTime=datetime.datetime.now())
session.add(command1)
session.commit()

#query via sqlalchemy orm
response = session.query(Logs).all()

for x in response:
    print (x.AccessTime)

#Close the connection
engine.dispose()

######################################
# Start Web Server                   #
######################################

httpserver_object = httpserver.httpserver(DOWNLOAD_FOLDER)

