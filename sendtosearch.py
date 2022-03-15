import meilisearch
import json
from json2table import convert
from bs4 import BeautifulSoup as bs
import os
import re
import pysftp as sftp
import requests
import time
from ftplib import FTP
from pathlib import Path
import ftplib
import decouple
from decouple import config

SEARCHCLIENT = config('SEARCHCLIENT')
SEARCHAPIKEY = config('SEARCHAPIKEY')
FTPSERVER = config('FTPSERVER')
FTPUSER = config('FTPUSER')
FTPPASS = config('FTPPASS')
FTPLOCATION = config('FTPLOCATION')


#client = meilisearch.Client('serverlocation', 'apikey')
client = meilisearch.Client(SEARCHCLIENT, SEARCHAPIKEY)
json_file = open('outputsearchready.json')
games = json.load(json_file)
client.delete_index('games')#deletes previous index due to the way meilisearch does indexes, it adds on top of, and updating doesn't work very well, so a good ole delete and create works fine.
client.index('games').add_documents(games)
try:
	json_file = open("outputcleaned.json")#json file to be used
	strings = json.load(json_file)#loads json
except:
	print('could not load json file.')
build_direction = "LEFT_TO_RIGHT"#table build option
table_attributes = {"style" : "width:100%", "class" : "alllinks"}#table attribute options
html = convert(strings, build_direction=build_direction, table_attributes=table_attributes)#converting to html table
#print(html)#can print if you wanna see it work lol
htmlfile = open("table.html", "w")#creates or opens table.html
htmlfile.write(html)#writes to table.html
htmlfile.close#saves table.html
try:
	with open('table.html', 'r') as f2:
		tablefile = f2.read()
except:
	print('table file not found, rerun totable.py to make it.')
	import totable
#aquire current html file
try:
	url = 'https://old.rezi.one'
	r = requests.get(url)
	time.sleep(20)
	htmlfile = open("index.html", "w")#creates index.html
	htmlfile.write(r.text)#writes to index.html
	htmlfile.close#saves index.html
	htmlfile = open("index.html", "r")
except:	print('site down or network not available; or python is having trouble writing to new index.')
#modify html
base = os.path.dirname(os.path.abspath(__file__))
html = open(os.path.join(base, 'index.html'))
soup = bs(html, 'html.parser')
soup.table.append(tablefile)
with open("index.html", "w") as outf:
    outf.write(soup.prettify(formatter=None))
#send html through sftp
#host = "192.168.0.200"
#port = 21
#username = "root"
#password = "Coolben11023"
#cnopts = sftp.CnOpts()
#cnopts.hostkeys = None
#with sftp.Connection(host=host, username=username, password=password, cnopts=cnopts) as sftp:
   #print("Connection succesfully established ... ")
#   sftp.cwd('/mnt/user/appdata/nginx/old.rezi.one/')  # Switch to a remote directory
#   sftp.put('index.html')
#sftp.close()
filename = "index.html"
ftp = ftplib.FTP(FTPSERVER)
ftp.login(FTPUSER, FTPPASS)
ftp.cwd(FTPLOCATION)
uploadfile= open('./index.html', 'rb')
ftp.storbinary('STOR ' + filename, uploadfile)