from bs4 import BeautifulSoup

def parse_html(content):
    return BeautifulSoup(content, 'html.parser')
