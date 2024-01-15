from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class Article:
    def __init__(self, elem) -> None:
        self.link = elem.get_attribute('href')
        span_elems = elem.find_elements(By.TAG_NAME, 'span')
        self.date = span_elems[0].text
        self.author = span_elems[1].text if len(span_elems) > 1 else ''
        self.text = ''
        self.title = ''

class FinamNewsParser:

    def collect_news(self, ticker, start = None, end = None, maxCount = None):
        return []