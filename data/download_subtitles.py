import time
import argparse

from bs4 import BeautifulSoup
import requests
from selenium import webdriver


def get_urls(num_pages):
    for i in range(num_pages):
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
    parser.add_argument("-n", "--num_pages", type=int, required=True, help="Need to get the number of pages")  # noqa
    args = parser.parse_args()
    return args


def execute_downloading(path_chromedriver, sleep_time, num_pages):
    elements_css_selector = [
        "input.downloadlink", "input.downloadlink", "a#logo",
    ]

    driver = webdriver.Chrome(path_chromedriver)

    for url in get_urls(num_pages):
        driver.get(url)
        for i in elements_css_selector:
            driver.find_element_by_css_selector(i).click()
        time.sleep(sleep_time)
    driver.close()


def main():
    args = argparser()
    execute_downloading(args.path_chromedriver, args.sleep, args.num_pages)


if __name__ == "__main__":
    main()
