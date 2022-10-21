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
import os
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
from scraper.spiders.scooterrepacks import ScooterRepacksSpider
from scraper.spiders.steamrip import SteamripSpider
from scraper.spiders.threedsroms import ThreeDSRomsSpider
from scraper.spiders.xcinsp import XciNspSpider

#time
now=datetime.now()
current_time = now.strftime("%H:%M:%S")
print(f"Time started: {current_time}.")
CRONMONITORING = config("CRONMONITORING")
#scraper
crawler = CrawlerProcess(get_project_settings())
crawler.crawl(AbandonwareSpider) # https://myabandonware.com
crawler.crawl(ArchiveSpider) # https://archive.org
crawler.crawl(FitgirlSpider) # https://fitgirl-repacks.site
crawler.crawl(GamesdriveSpider) # https://gamesdrive.net
crawler.crawl(GogSpider) # https://gog-games.com
crawler.crawl(MadloaderSpider) # https://madloader.com
crawler.crawl(NoPayStationSpider) # https://nopaystation.com
crawler.crawl(OvaGamesSpider) # https://ovagames.com
crawler.crawl(PokemonromSpider) # https://pokemonrom.net
crawler.crawl(ScooterRepacksSpider) # https://scooter-repacks.site
crawler.crawl(SteamripSpider) # https://steamrip.com
crawler.crawl(ThreeDSRomsSpider) # https://3dsroms.com
crawler.crawl(XciNspSpider) # https://xcinsp.com
crawler.start()
#meilisearch
SEARCHCLIENT = config("SEARCHCLIENT")
SEARCHCLIENTKEY = config("SEARCHCLIENTKEY")
client = meilisearch.Client(SEARCHCLIENT, SEARCHCLIENTKEY)
index = client.index('rezi')
csvfile = open('rezi.csv', 'r')
data = csvfile.read()
client.index('rezi').delete_all_documents()
index.add_documents_csv(data.encode('utf-8'))
# os.remove("rezi.csv")
# finishing
print("### Finished ###")
try:
	now=datetime.now()
	current_time = now.strftime("%H:%M:%S")
	requests.post(CRONMONITORING, data=f'Time finished: {current_time}.')
except requests.RequestException as e:
	print("Ping failed: %s" % e)

