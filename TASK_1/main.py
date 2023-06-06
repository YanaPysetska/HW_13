import requests
import re
from bs4 import BeautifulSoup
import argparse
class LinkChecker:
    def __init__(self, url=None):
        if url is None:
            self.get_link()
        else:
            self.url = url
        self.valid_urls = []
        self.invalid_urls = []

    def get_link(self):
        parser = argparse.ArgumentParser(description='URL parser')
        parser.add_argument('-url', metavar='-url', type=str, help='Enter your URL')
        args = parser.parse_args()

        url = args.url
        if self.check_link(url):
            self.url=url
        else:
            print('Линка не валидная')

    def check_link(self, url):
        url_pattern = re.compile(
            r'^(https?://)?'  # протокол
            r'((([a-zA-Z0-9_\-]+)\.)+[a-zA-Z]{2,63}|'  # доменне ім'я
            r'(([0-9]{1,3}\.){3}[0-9]{1,3}))'  # або IP-адреса
            r'(:[0-9]{1,5})?'  # порт
            r'(/.*)?$'  # шлях
        )
        return re.match(url_pattern, url)

    def extract_links(self):
        reqs = requests.get(self.url)
        soup = BeautifulSoup(reqs.text, 'html.parser')
        for i in soup.find_all("a"):
            data = i.get('href')
            if data.startswith('http://') or data.startswith('https://'):
                response = requests.get(data)
                site_status_code = response.status_code
                if site_status_code != 200:
                    self.invalid_urls.append(data)
                else:
                    self.valid_urls.append(data)
            elif not data.startswith('/'):
                self.invalid_urls.append(data)

    def save_valid_urls(self):
        with open("valid_urls.txt", "w") as valid_file:
            for url in self.valid_urls:
                valid_file.write(url + "\n")

    def save_invalid_urls(self):
        with open("invalid_urls.txt", "w") as invalid_file:
            for url in self.invalid_urls:
                invalid_file.write(url + "\n")
    def print_error_message(self, url):
        print(f"Недопустимая ссылка: {url}")

checker = LinkChecker()
checker.extract_links()
checker.save_valid_urls()
checker.save_invalid_urls()