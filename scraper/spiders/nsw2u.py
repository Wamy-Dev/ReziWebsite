from scrapy import Selector
import scrapy
from scraper.items import GameItem
from datetime import datetime
from uuid import uuid4
from urllib.parse import unquote
import undetected_chromedriver.v2 as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyvirtualdisplay import Display
disp = Display()
disp.start()
options = uc.ChromeOptions()
# options.add_argument('--headless')
# options.add_argument("--disable-gpu")
# options.add_argument("--no-sandbox")
# options.add_argument("--disable-dev-shm-usage")
# options.add_argument("--disable-setuid-sandbox")
# options.add_argument("--disable-software-rasterizer")
driver = uc.Chrome(options=options)

class Nsw2uSpider(scrapy.Spider):

    name = "nsw2uspider"
    allowed_domains = ["toscrape.com"]

    def start_requests(self):
        url = "http://quotes.toscrape.com"
        yield scrapy.Request(url=url, callback=self.parse)
        
    def parse(self, response):
        driver.get("https://nsw2u.com/switch-posts")
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "az-columns")))
        sel = Selector(text=driver.page_source)
        for post in sel.css("ul.az-columns li"):
            game_item = GameItem()
            link = post.css("a ::attr(href)").get()
            title = post.css("a ::text").get()
            game_item["link"] = link
            game_item["title"] = unquote(title.strip())
            game_item["id"] = str(uuid4()) + datetime.now().strftime('%Y%m-%d%H-%M%S-')
            game_item["icon"] = "Switch"
            game_item["system"] = ["switch", "nintendo switch", "nswitch"]
            yield game_item