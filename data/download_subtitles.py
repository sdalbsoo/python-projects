import time
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
    driver = webdriver.Chrome("/Users/Sdalbsoo/Downloads/chromedriver")
    elements_css_selector = [
        "input.downloadlink", "input.downloadlink", "a#logo",
    ]

    for url in get_url():
        driver.get(url)
        for i in elements_css_selector:
            driver.find_element_by_css_selector(i).click()
        time.sleep(5)
    driver.close()


if __name__ == "__main__":
    main()
