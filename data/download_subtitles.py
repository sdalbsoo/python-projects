import time

import argparse
from bs4 import BeautifulSoup
import requests
from selenium import webdriver


def get_url():
    list_urls = []

    for i in range(10):
        resp = requests.get("https://english-subtitles.org/page/{}".format(i+1))  # noqa
        source = resp.text
        soup = BeautifulSoup(source, "lxml")
        parsed = [i for i in soup.find_all("div", attrs={"class": "tbl"})]
        for j in parsed:
            list_urls.append(j.find('a')['href'])
    return list_urls


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path_chromedriver", type=str, required=True, help="Need to get path of chromedriver")  # noqa
    parser.add_argument("-s", "--sleep", type=int, required=True, help="Need to get sleep time")  # noqa
    args = parser.parse_args()

    path = args.path_chromedriver
    sleep_time = args.sleep

    driver = webdriver.Chrome(path)
    elements_css_selector = [
        "input.downloadlink", "input.downloadlink", "a#logo",
    ]
    for url in get_url():
        driver.get(url)
        for i in elements_css_selector:
            driver.find_element_by_css_selector(i).click()
        time.sleep(sleep_time)
    driver.close()


if __name__ == "__main__":
    main()
