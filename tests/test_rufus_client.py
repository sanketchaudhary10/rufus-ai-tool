import pytest
from rufus_client import RufusClient

def test_scrape():
    client = RufusClient()
    url = "https://www.example.com"
    instructions = "Find contact information."
    result = client.scrape(url, instructions)
    assert result is not None
    assert "data" in result
