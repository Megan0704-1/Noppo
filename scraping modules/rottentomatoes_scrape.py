from bs4 import BeautifulSoup
from lxml import etree
import requests
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


def expand_shadow_element(browser, element):
    shadow_root = browser.execute_script(
        'return arguments[0].shadowRoot', element)
    return shadow_root


def scrape_movie_page(rt_url):
    try:
        chrome_options = Options()
        chrome_options.headless = True
        chromedriver = webdriver.Chrome(
            ChromeDriverManager().install(), options=chrome_options)
        with chromedriver as browser:
            browser.get(rt_url)
            root = browser.find_element_by_tag_name('score-board')
            score_board = expand_shadow_element(browser, root)
            tm_container = score_board.find_element(
                By.CSS_SELECTOR, '.tomatometer-container')
            ad_container = score_board.find_element(
                By.CSS_SELECTOR, '.audience-container')
            tm_score = expand_shadow_element(browser,
                                             tm_container.find_element(By.CSS_SELECTOR, 'score-icon-critic'))
            ad_score = expand_shadow_element(browser, ad_container.find_element(
                By.CSS_SELECTOR, 'score-icon-audience'))
            tm_score = tm_score.find_element(By.CSS_SELECTOR, 'div').find_elements(
                By.CSS_SELECTOR, 'span')[1].text
            ad_score = ad_score.find_element(By.CSS_SELECTOR, 'div').find_elements(
                By.CSS_SELECTOR, 'span')[1].text
            browser.close()
        return (tm_score[1].text, ad_score[1].text)
    except Exception as err:
        return err
    return 'not found in google'


def scrape_rotten_tomatoes(drama):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'}
    try:
        page = requests.get(
            'https://www.google.com/search?q={}'.format(drama + '+rotten+tomatoes'), headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')
        dom = etree.HTML(str(soup))
        try:
            rt_url = dom.xpath(
                '//div[@class="g"][1]/div/div/div/div/div[1]/a/@href')[0]
        except Exception as err:
            return err
        if 'rottentomatoes.com' in rt_url:
            if '.com/m/' in rt_url:
                return scrape_movie_page(rt_url)
            else:
                try:
                    page = requests.get(rt_url, headers=headers)
                    soup = BeautifulSoup(page.content, "html.parser")
                    tm_score = soup.find(
                        'span', {'data-qa': 'tomatometer'}).text.replace(' ', '').replace('\n', '')
                    ad_score = soup.find(
                        'span', {'data-qa': 'audience-score'}).text.replace(' ', '').replace('\n', '')
                    return (tm_score, ad_score)
                except Exception as err:
                    return err
    except:
        return 'not found in google'
