import time
from bs4 import BeautifulSoup
import requests
from selenium import webdriver

list_urls = []
for i in range(10):
    resp = requests.get("https://english-subtitles.org/page/{}".format(i+1))
    source = resp.text
    soup = BeautifulSoup(source, "lxml")
    parsed = [i for i in soup.find_all("div", attrs={"class": "tbl"})]
    for j in parsed:
        list_urls.append(j.find('a')['href'])

driver = webdriver.Chrome("/Users/Sdalbsoo/Downloads/chromedriver")
for i in list_urls:
    driver.get(i)
    driver.find_element_by_css_selector("input.downloadlink").click()
    driver.find_element_by_css_selector("input.downloadlink").click()
    driver.find_element_by_css_selector("a#logo").click()
    time.sleep(5)
driver.close()
