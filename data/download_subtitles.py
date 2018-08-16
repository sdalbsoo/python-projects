import time
import argparse

from bs4 import BeautifulSoup
import requests
from selenium import webdriver


def get_urls():
    for i in range(10):
        resp = requests.get("https://english-subtitles.org/page/{}".format(i+1))  # noqa
        source = resp.text
        soup = BeautifulSoup(source, "lxml")
        parsed = [k for k in soup.find_all("div", attrs={"class": "tbl"})]
        for j in parsed:
            yield j.find("a")["href"]


def argparser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path_chromedriver", type=str, required=True, help="Need to get path of chromedriver")  # noqa
    parser.add_argument("-s", "--sleep", type=int, required=True, help="Need to get sleep time")  # noqa
    args = parser.parse_args()
    return args


def execute_downloading():
    elements_css_selector = [
        "input.downloadlink", "input.downloadlink", "a#logo",
    ]

    args = argparser()
    driver = webdriver.Chrome(args.path_chromedriver)

    for url in get_urls():
        driver.get(url)
        for i in elements_css_selector:
            driver.find_element_by_css_selector(i).click()
        time.sleep(args.sleep)
    driver.close()


def main():
    execute_downloading()


if __name__ == "__main__":
    main()
