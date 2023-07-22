import requests
import re
import time
import telegram_send
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By


with open('/home/a/Downloads/flats.txt') as f:
    old_flats = f.readlines()

old_flats = set(old_flats)

# start web browser
options = webdriver.ChromeOptions()
options.add_argument("headless")
options.add_argument('--disable-blink-features=AutomationControlled')

driver = webdriver.Chrome(options=options)

new_flats = []

# put you search urls here (they are to be sorted by most recently created)
url_immonet = ""
url_immowelt = ""
url_wg_gesucht = ""
url_ebay = ""

# Load the webpage
driver.get(url_immonet)
time.sleep(5)
html = driver.page_source
# Parse the HTML with BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')
# Extract href links
links = soup.find_all('a', href=True)

# Print the links
for link in links:
    if "expose" in link["href"]:
        if link["href"] + "\n" not in old_flats:
            print("NEW FLAT ", link["href"])
            new_flats.append(link["href"])
   

# check immowelt
print("check immowelt")
r = requests.get(url_immowelt)
soup = BeautifulSoup(r.text, 'html.parser')
for flat in soup.find_all('a', href=True):
    link = flat["href"]
    if "expose" in link:
        if link + "\n" not in old_flats:
            print("NEW FLAT ", link)
            new_flats.append(link)

# check wg-gesucht
print("check wg-gesucht")
r = requests.get(url_wg_gesucht)
soup = BeautifulSoup(r.text, 'html.parser')
regex = re.compile("\.[0-9]{3,}.html$")
for flat in soup.find_all('a', href=True):
    if regex.search(flat["href"]):
        link = "https://www.wg-gesucht.de/"+flat["href"]
        if link + "\n" not in old_flats:
            print("NEW FLAT ", link)
            new_flats.append(link)
            
# check ebay
print("check ebay-kleinanzeigen")
driver.get(url_ebay)
html = driver.page_source.split("Alternative Anzeigen in der Umgebung")[0]
time.sleep(2)
soup = BeautifulSoup(html, 'html.parser')
for flat in soup.find_all('a', href=True):
    if not ("/s-anzeige/" in flat["href"]): continue
    link = "https://www.ebay-kleinanzeigen.de"+flat["href"]
    if link + "\n" not in old_flats:
        print("NEW FLAT ", link)
        new_flats.append(link)    

if(new_flats != []):
    print("sending telegram msg")
    telegram_send.send(messages=["Es wurden neue Wohnungen gefunden!"])
    telegram_send.send(messages=new_flats)
    with open('/home/a/Downloads/flats.txt', "a") as f:
        for flat in new_flats:
            f.writelines([flat + "\n"])

else:
    print("No new flats")
    sdriver.quit()
