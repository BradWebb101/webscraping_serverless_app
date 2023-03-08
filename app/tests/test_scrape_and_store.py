import os
import boto3
import pickle
from app.utils.aws_helpers import S3
from datetime import datetime
from unittest.mock import Mock, patch
import requests
import pytest
from bs4 import BeautifulSoup
from scrape_and_store.scrape_and_store import ScrapeAndStore


@pytest.fixture
def scraper():
    url = 'https://www.example.com'
    return ScrapeAndStore(url)

@patch('requests.get')
def test_scrape(mock_get, scraper):
    mock_get.return_value.content = '<html><body><h1>Test</h1></body></html>'
    scraper.scrape()
    assert isinstance(scraper.soup, BeautifulSoup)
    assert scraper.soup.h1.string == 'Test'

@patch('boto3.client')
def test_store(mock_client, scraper):
    mock_s3 = Mock()
    mock_client.return_value = mock_s3
    scraper.soup = BeautifulSoup('<html><body><h1>Test</h1></body></html>', 'html.parser')
    scraper.store()
    key = f"pickle/{scraper.key}"
    mock_s3.put_object.assert_called_once_with(Bucket='example-bucket', Key=key, Body=pickle.dumps(scraper.soup))

def test_main(monkeypatch, scraper):
    monkeypatch.setenv('URL', 'https://www.example.com')
    scraper.scrape = Mock()
    scraper.store = Mock()
    main()
    scraper.scrape.assert_called_once()
    scraper.store.assert_called_once()
