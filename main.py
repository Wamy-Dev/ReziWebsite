# Welcome to Rezi!
#    ____             _ 
#   / __ \___  ____  (_)
#  / /_/ / _ \/_  / / / 
# / _, _/  __/ / /_/ /  
# /_/ |_|\___/ /___/_/   
# Rezi was written in Python 3.8.10 on VSCode.
# Please visit the github at https://github.com/Wamy-Dev/ReziWebsite

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from datetime import datetime
import requests
import meilisearch
from decouple import config
import requests
import os
import time
import json
from notify import notify
import csv
#input file
file = requests.get("https://raw.githubusercontent.com/Wamy-Dev/ReziWebsite/main/input.json")
with open("input.json", "w") as json_file:
	json.dump(file.json(), json_file, indent=4)
# scrapers
from scraper.spiders.abandonware import AbandonwareSpider
from scraper.spiders.archive import ArchiveSpider
from scraper.spiders.fitgirlrepacks import FitgirlSpider
from scraper.spiders.gamesdrive import GamesdriveSpider
from scraper.spiders.gog import GogSpider
from scraper.spiders.madloader import MadloaderSpider
from scraper.spiders.nopaystation import NoPayStationSpider
from scraper.spiders.ovagames import OvaGamesSpider
from scraper.spiders.pokemonrom import PokemonromSpider
from scraper.spiders.steamrip import SteamripSpider
from scraper.spiders.threedsroms import ThreeDSRomsSpider
from scraper.spiders.xcinsp import XciNspSpider
from scraper.spiders.playablearchive import ArchivePlayableSpider
from scraper.spiders.kaoskrew import KaosKrewSpider
from scraper.spiders.cpg import CPGSpider
from scraper.spiders.gamebounty import GameBountySpider
from scraper.spiders.gamedrive import GameDriveSpider
from scraper.spiders.games4u import Games4USpider
#time
now=datetime.now()
current_time = now.strftime("%H:%M:%S")
print(f"Time started: {current_time}.")
CRONMONITORING = config("CRONMONITORING")
#scraper
if os.path.exists("rezi.csv"):
  	os.remove("rezi.csv")
else:
  print("First run initiated.")
crawler = CrawlerProcess(get_project_settings())
crawler.crawl(AbandonwareSpider) # https://myabandonware.com
crawler.crawl(ArchiveSpider) # https://archive.org
crawler.crawl(FitgirlSpider) # https://fitgirl-repacks.site
crawler.crawl(GamesdriveSpider) # https://gamesdrive.net
crawler.crawl(GameDriveSpider) #https://gamedrive.org (NOT gamesdrive.net)
crawler.crawl(GogSpider) # https://gog-games.com
crawler.crawl(MadloaderSpider) # https://madloader.com
crawler.crawl(NoPayStationSpider) # https://nopaystation.com
crawler.crawl(OvaGamesSpider) # https://ovagames.com
crawler.crawl(PokemonromSpider) # https://pokemonrom.net
crawler.crawl(SteamripSpider) # https://steamrip.com
crawler.crawl(ThreeDSRomsSpider) # https://3dsroms.com
crawler.crawl(XciNspSpider) # https://xcinsp.com
crawler.crawl(ArchivePlayableSpider) # https://archive.org
crawler.crawl(KaosKrewSpider) # https://kaoskrew.org
crawler.crawl(CPGSpider) # https://cpgrepacks.site
crawler.crawl(GameBountySpider) # https://gamebounty.world
crawler.crawl(Games4USpider) # https://games4u.org
crawler.start()
#meilisearch
SEARCHCLIENT = config("SEARCHCLIENT")
SEARCHCLIENTKEY = config("SEARCHCLIENTKEY")
client = meilisearch.Client(SEARCHCLIENT, SEARCHCLIENTKEY)
index = client.index('rezi')
csvfile = open('rezi.csv', 'r', encoding='utf-8')
data = csvfile.read()
csvfile.seek(0)
index.delete_all_documents()
time.sleep(5)
result = index.add_documents_csv(data.encode('utf-8'))
print(result)
csvfile = csv.reader(csvfile)

#finishing
notify(now, datetime.now(), sum(1 for row in csvfile))
try:
	now=datetime.now()
	current_time = now.strftime("%H:%M:%S")
	requests.post(CRONMONITORING, data=f'Time finished: {current_time}.')
except requests.RequestException as e:
	print("Ping failed: %s" % e)
print("### Finished ###")

