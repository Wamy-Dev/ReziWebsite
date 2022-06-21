#Libraries and importing
from bs4 import BeautifulSoup
import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import random
import json
import time
from decouple import config
import requests
from os import getcwd
#
print('starting process')
#getting updated input file
url = "https://raw.githubusercontent.com/Wamy-Dev/ReziWebsite/main/Input%20Data.txt"
r = requests.get(url)
data = open("./components/Input Data.txt", "wb")
data.write(r.content)
data.close()
#setting up chrome settings
chrome_options = uc.ChromeOptions()
chrome_options.add_extension('./resources/ublockorigin.crx')
chrome_options.add_extension('./resources/popupblockerpro.crx')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.arguments.extend(["--no-sandbox", "--disable-setuid-sandbox"])
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36")
wd = uc.Chrome(chrome_options) #if in docker container
json_data={}
#getting the links and setting up json
def link_container(site_name,container_tag,class_tag,html,domain):
    soup=BeautifulSoup(html,'html.parser')
    containers=soup.find_all(container_tag,class_=class_tag)
    for container in containers:
        links=container.find_all("a")
        for link in links:
            if(domain not in link['href']):  
                json_data[name].append(domain+link['href'])
            else:
                json_data[name].append(link['href'])
            #print(link['href'])#add domain+link
#to getting the html of webpage
def request_page(url):
    wd.get(url)
    time.sleep(5)
    return wd.page_source
#to get the next element
def return_next_ele(html,check_element,next_page):
    if(check_element != "null"):
        temp=[]
        retries = 1
        while retries <= 1:
            try:
                temp = WebDriverWait(wd,10).until(EC.element_to_be_clickable((By.XPATH, '//button[@id="{}"]'.format(check_element))))
                temp.click()
                break
            except TimeoutException:
                retries += 1
    next=[]
    retries = 1
    while retries <= 2:
        try:
            next = WebDriverWait(wd,10).until(EC.element_to_be_clickable((By.XPATH, '//a[@class="{}"]'.format(next_page))))
            next = wd.find_elements(By.XPATH,'//a[@class="{}"]'.format(next_page))[-1]
            break
        except TimeoutException:
            retries += 1
    # next=wd.find_element(By.XPATH,'//a[@class="lcp_nextlink"]')
    return next
#getting data from input file
input_file=open('./components/Input Data.txt','r')
name=input_file.readline().replace("\n","")
json_data[name]=[]
while (True):
    url=input_file.readline().replace("\n","")
    domain=input_file.readline().replace("\n","")
    container=input_file.readline().replace("\n","")
    clas=input_file.readline().replace("\n","")
    next_link=input_file.readline().replace("\n","")
    bypass=input_file.readline().replace("\n","")
    #getting page and getting links for output file
    html=request_page(url)
    next=return_next_ele(html,bypass,next_link)
    index=0
    old_url=""
    current_url=wd.current_url
    while(next is not None and next is not  []):
        if(old_url == current_url):
            break
        else:
            old_url=current_url
        index+=1
        link_container(name,container,clas,wd.page_source,domain)
        time.sleep(random.randint(1,5))
        if(next == []):
            break
        next.click()
        html=wd.page_source
        next=return_next_ele(html,bypass,next_link)
        current_url=wd.current_url
    name=input_file.readline().replace("\n","")
    if(name not in json_data):
        json_data[name]=[]
    if not name: break
input_file.close()
#outputting the data to Output.json
output_file=open("./components/output.json","w")
json_string=json.dumps(json_data)
output_file.write(json_string)
output_file.close()
wd.close()
import cleaner
