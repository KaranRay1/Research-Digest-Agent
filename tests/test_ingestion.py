# Ingestion tests
import pytest
from src.ingestion import Ingestion
import responses

@responses.activate
def test_fetch_url_unreachable():
    url = "https://nonexistent-url.com"
    responses.add(responses.GET, url, status=404)
    
    result = Ingestion.fetch_url(url)
    assert result is None

@responses.activate
def test_fetch_url_empty_content():
    url = "https://empty.com"
    responses.add(responses.GET, url, body="", status=200)
    
    result = Ingestion.fetch_url(url)
    assert result["content"] == ""

def test_read_nonexistent_file():
    result = Ingestion.read_file("nonexistent.txt")
    assert result is None
