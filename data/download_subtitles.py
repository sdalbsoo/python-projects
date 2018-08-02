import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

driver = webdriver.Chrome("/Users/Sdalbsoo/Downloads/chromedriver")
driver.get("https://english-subtitles.org/")

open_subtitle = "//div[@class='opener']"
driver.find_element_by_xpath(open_subtitle).click()

ready_subtitle= "//input[@class='downloadlink']"
driver.find_element_by_xpath(ready_subtitle).click()

download_subtitle= "//input[@class='downloadlink' and @type='submit']"
driver.find_element_by_xpath(download_subtitle).click()

go_home = "//a[@id='logo']"
driver.find_element_by_xpath(go_home).click()

time.sleep(10)
driver.quit()
