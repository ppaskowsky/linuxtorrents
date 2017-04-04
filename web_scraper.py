from __future__ import print_function
import httplib2, os, uuid, shutil, requests, bs4, re

from apiclient.http import MediaIoBaseDownload
from apiclient.http import MediaFileUpload
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from oauth2client.service_account import ServiceAccountCredentials

class scraper:

	#function to search for torrent files using beautifulsoup
	#imputs are url, search term, and if the torrent link is static or dynamic (if it changes per release)
	def scrape(self,url,find,static,DOWNLOAD_FOLDER):

		#download html
		response = requests.get(url)
		#print response

		#read content of html
		data = response.text
		#print data

		#load html into BeautifulSoup
		soup = bs4.BeautifulSoup(data,"html.parser")
		#print soup

		#serach for all matching links and download them

		if static == 'true':
		#search for a certain file name using regex
			for link in soup.find_all(href=re.compile(find)):
				#save torrent file namein variable
				downloadurl = link.get('href')
				#concatinate with url and download
				downloadurl = url + downloadurl
				self.downloadfile(downloadurl,DOWNLOAD_FOLDER)
		else:
		#search for a certain class on a website, containing links
			for link in soup.find_all(class_= find):
				#save torrent file namein variable
				downloadurl = link.get('href')
				#download file
				self.downloadfile(downloadurl,DOWNLOAD_FOLDER)

	#function to download files
	def downloadfile(self,url,DOWNLOAD_FOLDER):
		print('Downloading %s...' % url)
		torrentfile = requests.get(url)
		#write torrentfile to disk
		downloadfile = open(os.path.join(DOWNLOAD_FOLDER, os.path.basename(url)), 'wb')
		for chunk in torrentfile.iter_content(100000):
			downloadfile.write(chunk)
		downloadfile.close()


