import pytest
from rufus_api import RufusAPI

def test_api_scrape():
    api = RufusAPI()
    url = "https://www.example.com"
    instructions = "Find pricing information."
    result = api.scrape(url, instructions)
    assert result is not None
    assert "url" in result
    assert "data" in result
