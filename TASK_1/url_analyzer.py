#мой проверочный сайт https://bpa.com.ua/
import requests
import re
from bs4 import BeautifulSoup

class LinkChecker:
    def __init__(self, url=None):
        if url is None:
            self.url = input("Введите URL: ")
        else:
            self.url = url
        self.valid_urls = []
        self.invalid_urls = []

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
            else:
                self.invalid_urls.append(data)
    def check_link(self, url):
        if re.match(r'^(http|https)://', url) or url.endswith('.com') or url.endswith('.py'):
            response = requests.get(url)
            if response.status_code == 200:
                return True
            return False
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