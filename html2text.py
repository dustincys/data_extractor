import argparse
from goose3 import Goose
from goose3.text import StopWordsChinese
import re
import requests

class extractor:
    def __init__(self):
        self.g_cn = Goose({'stopwords_class': StopWordsChinese})
        self.g_en = Goose()
        pass

    def __contains_chinese(self, text):
        pattern = re.compile(r'[\u4e00-\u9fff]')  # Range for Chinese characters
        return bool(pattern.search(text))

    def __get_html(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for bad status codes
            return response.text  # Return the raw HTML content
        except requests.RequestException as e:
            print(f"Failed to retrieve HTML: {e}")
            return None

    def url(self, url):
        html_string = self.__get_html(url)
        return self.html(html_string)
        pass

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
