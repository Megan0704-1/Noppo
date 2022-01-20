from bs4 import BeautifulSoup
from lxml import etree
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import requests
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'}


def scrape_douban(drama):
    try:
        chrome_options = Options()
        chrome_options.headless = True
        chromedriver = webdriver.Chrome(
            ChromeDriverManager().install(), options=chrome_options)
        with chromedriver as browser:
            browser.get(
                'https://www.google.com/search?q={}'.format('+'.join(drama.split(' ')+['豆瓣'])))
            try:
                soup = BeautifulSoup(browser.page_source, "html.parser")
                dom = etree.HTML(str(soup))
                douban_url = dom.xpath(
                    '//div[@class="g"][1]/div/div/div/div/div/a/@href')[0]
            except:
                try:
                    soup = BeautifulSoup(browser.page_source, "html.parser")
                    dom = etree.HTML(str(soup))
                    douban_url = dom.xpath(
                        '//div[@class="g"][1]/div/div/div/a/@href')[0]
                except Exception as e:
                    print(e)
                    return 'not found in google'
            if 'douban.com' in douban_url:
                if 'review' in douban_url:
                    douban_url = dom.xpath(
                        '//div[@class="g"][1]/div[2]/ul/li/div/div/div/div/div/a/@href')[0]
                try:
                    time.sleep(2)
                    browser.get(douban_url)
                    soup = BeautifulSoup(browser.page_source, "html.parser")
                    score = soup.find('strong').text
                    info = soup.find('span', {'property': 'v:summary'}).text
                    image = soup.find('img', {'rel': 'v:image'})['src']
                    browser.close()
                    return {'score': score, 'info': info, 'image': image}
                except Exception as err:
                    browser.close()
                    return err
            browser.close()
    except Exception as e:
        return e
