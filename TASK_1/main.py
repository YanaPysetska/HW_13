import requests
import re
from bs4 import BeautifulSoup
import argparse
import PyPDF2
import logging
import time


class LinkChecker:
    def __init__(self, url=None, pdf_path=None):
        if url is None and pdf_path is None:
            self.get_input()
        else:
            self.url = url
            self.pdf_path = pdf_path
        self.valid_urls = []
        self.invalid_urls = []

    def get_input(self):
        parser = argparse.ArgumentParser(description='Parser')
        parser.add_argument('-url', metavar='-url', type=str, help='Enter your URL')
        parser.add_argument('--pdf', metavar='-url', type=str, help='Enter your path to file')
        args = parser.parse_args()

        self.url = args.url
        self.pdf_path = args.pdf

        if self.url is None and self.pdf_path is None:
            logging.warning('Values url or pdf is not provided')
            print('Введи URL или путь к PDF файлу')
            return

        if self.url is not None and not self.check_link(self.url):
            print('Invalid URL.')
            return

    def check_link(self, url):
        url_pattern = re.compile(
            r'^(https?://)?'  # протокол
            r'((([a-zA-Z0-9_\-]+)\.)+[a-zA-Z]{2,63}|'  # доменне ім'я
            r'(([0-9]{1,3}\.){3}[0-9]{1,3}))'  # або IP-адреса
            r'(:[0-9]{1,5})?'  # порт
            r'(/.*)?$'  # шлях
        )
        return re.match(url_pattern, url)

    def find_url(self, string):
        regex = r"(https?://\S+)"
        urls = re.findall(regex, string)
        return urls

    def extract_links_from_url(self):
        if self.url is not None:
            start_time = time.perf_counter()
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
            end_time = time.perf_counter()
            execution_time = end_time - start_time

            logging.info(f'Execution time URL -> {execution_time:.6f} sec.')
    def extract_links_from_pdf(self):
        if self.pdf_path is not None:
            start_time = time.perf_counter()
            readPDF = PyPDF2.PdfReader(self.pdf_path)
            for page_no in range(len(readPDF.pages)):
                page = readPDF.pages[page_no]
                text = page.extract_text()
                urls = self.find_url(text)
                for url in urls:
                    try:
                        if self.check_link(url):
                            response = requests.get(url)
                            response.raise_for_status()
                            self.valid_urls.append(url)
                        else:
                            self.invalid_urls.append(url)
                    except requests.exceptions.RequestException:
                        self.invalid_urls.append(url)
            end_time = time.perf_counter()
            execution_time = end_time - start_time
            logging.info(f'Execution time PDF path -> {execution_time:.6f} sec.')

    def save_valid_urls(self):
        with open("valid_urls.txt", "w") as valid_file:
            for url in self.valid_urls:
                valid_file.write(url + "\n")

    def save_invalid_urls(self):
        with open("invalid_urls.txt", "w") as invalid_file:
            for url in self.invalid_urls:
                invalid_file.write(url + "\n")


logging.basicConfig(level=logging.INFO, filename='my_log.log',
                    filemode='w', format="%(asctime)s;%(levelname)s;%(message)s")

checker = LinkChecker()
checker.extract_links_from_url()
checker.extract_links_from_pdf()
checker.save_valid_urls()
checker.save_invalid_urls()
