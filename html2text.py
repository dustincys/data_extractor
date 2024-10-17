import argparse
import re

from goose3 import Goose
from goose3.text import StopWordsChinese
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class extractor:
    def __init__(self):
        self.g_cn = Goose({'stopwords_class': StopWordsChinese})
        self.g_en = Goose()
        self.headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

    def __contains_chinese(self, text):
        pattern = re.compile(r'[\u4e00-\u9fff]')  # Range for Chinese characters
        return bool(pattern.search(text))

    def __get_html(self, url):
        try:
            options = Options()
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')
            options.add_argument('--no-sandbox')
            options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
            driver = webdriver.Chrome(options=options)

            driver.get(url)
            page_source = driver.page_source
            driver.quit()
            return page_source  # Return the raw HTML content
        except Exception as e:
            print(f"Failed to retrieve HTML: {e}")
            return None

    def url(self, url):
        html_string = self.__get_html(url)
        return self.html(html_string)

    def html(self, html_string):
        html_string = html_string.strip(" \n")
        if html_string == "":
            return ""

        if self.__contains_chinese(html_string):
            g = self.g_cn
        else:
            g = self.g_en

        article = g.extract(raw_html = html_string)
        return article.cleaned_text.strip(" \n")

    def html_file(self, html_file):
        with open(html_file, 'r') as file:
            html_string = file.read()
            return self.html(html_string = html_string)

def main():
    parser = argparse.ArgumentParser(description = 'format string vector')
    parser.add_argument('--string', dest='inString', default = "", help='input string')
    parser.add_argument('--file', dest='inFile', default = "", help='input string File')
    parser.add_argument('--url', dest='inURL', default = "", help='input URL')
    args = parser.parse_args()

    inString = args.inString.strip(" \n")
    inFile = args.inFile.strip(" \n")
    inURL = args.inURL.strip(" \n")

    reString = ""
    e = extractor()
    if inString != "":
        reString = e.html(inString)
    elif inFile != "":
        reString = e.html_file(inFile)
    elif inURL != "":
        reString = e.url(inURL)

    print(reString)

if __name__ == '__main__':
    main()
