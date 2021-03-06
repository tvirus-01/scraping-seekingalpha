from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import requests
import time
import os
import csv

root_url = "https://seekingalpha.com"
query = "stock repurchase program"
url = "https://seekingalpha.com/search?q="+query.replcae(" ", "+")
chrome_driver_path = "/usr/lib/chromium-browser/chromedriver" #add your own driver path

opts = Options()
opts.add_argument("--headless")
opts.add_argument("--no-sandbox")
opts.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36")

driver = webdriver.Chrome(chrome_driver_path, options=opts)

driver.get(url)

time.sleep(5)

soup = BeautifulSoup(driver.page_source, 'lxml')

result_list = soup.find("div", {"id":"result_list"})

result_page = result_list.find("div", {"class":"result-pages"})

fields = ['Title', 'Link', 'MetaData', 'Summary']
csv_rows = []

for a in result_page.find_all("a"):
    link = a['href']
    new_url = url+link
    
    driver.get(new_url)
    time.sleep(5)

    new_soup = BeautifulSoup(driver.page_source, 'lxml')
    new_result_list = new_soup.find("div", {"id":"result_list"})

    items = new_result_list.find_all("li")

    for item in items:
        item_link = item.find("div", {"class":"item-link"})
        item_link_a = item_link.find("a")
        item_meta = item.find("div", {"class":"item-metadata"})
        item_summary = item.find("div", {"class":"item-summary"})

        name = item_link_a.text.replace("  ", "").replace("\n", "")
        link = root_url+item_link_a['href']
        metadata = item_meta.text.replace(" ", "")
        summary = item_summary.text
    
        csv_rows.append([str(name), str(link), str(metadata), str(summary)])

with open("SeekingAlpha.csv", 'w') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(fields)
    csvwriter.writerows(csv_rows)

print("Done")