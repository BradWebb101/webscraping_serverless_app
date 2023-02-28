import os
import requests
from bs4 import BeautifulSoup
import boto3
from datetime import datetime
import pickle
from app.utils.aws_helpers import S3    

class ScrapeAndStore:

    def __init__(self, url):
        self.url = url
        self.key = datetime.now()

    def scrape(self):
        response = requests.get(self.url)
        self.soup = BeautifulSoup(response.content, 'html.parser')
    
    def store(self) -> None:
        bucket_name = f"{self.url.split('.')[1]}-bucket"
        key = f"pickle/{self.key}"
        S3().put(Bucket=bucket_name, Key=key, Body=pickle.dumps(self.soup))

def main():
    url = os.getenv('URL')
    scraper = ScrapeAndStore(url).scrape()
    scraper.store()

if __name__ == '__main__':
    main()