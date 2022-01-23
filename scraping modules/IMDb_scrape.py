from bs4 import BeautifulSoup
from lxml import etree
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import requests
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'}


def scrape_imdb(drama):
    try:
        chrome_options = Options()
        chrome_options.headless = True
        chromedriver = webdriver.Chrome(
            ChromeDriverManager().install(), options=chrome_options)
        with chromedriver as browser:
            browser.get(
                'https://www.google.com/search?q={}'.format(drama + 'imdb'))
            soup = BeautifulSoup(browser.page_source, 'html.parser')
            dom = etree.HTML(str(soup))
            try:
                imdb_url_0 = dom.xpath(
                    '//div[@class="g"][1]/div/div/div[1]/a/@href')[0]
                imdb_url_1 = dom.xpath(
                    '//div[@class="g"][1]/div/div/div/div/div[1]/a/@href')[0]
                imdb_url_2 = dom.xpath(
                    '//div[@class="g"][1]/div[2]/ul/li/div/div/div/div/div[1]/a/@href')[0]
            except:
                pass
            try:
                if 'imdb.com' in imdb_url_0:
                    page = requests.get(imdb_url_0, headers=headers)
                elif 'releaseinfo' in imdb_url_1:
                    page = requests.get(imdb_url_2, headers=headers)
                else:
                    page = requests.get(imdb_url_1, headers=headers)
                soup = BeautifulSoup(page.content, "html.parser")
                score = soup.find(
                    'span', {'class': 'AggregateRatingButton__RatingScore-sc-1ll29m0-1 iTLWoV'}).text
                name = soup.find('h1').text
                print(name, score)
                return {'name': drama, 'score': score}
            except:
                pass
