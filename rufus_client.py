import asyncio
from spacy import load
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
from pydantic import BaseModel
from utils.nlp_utils import load_nlp_model
from utils.scraping_utils import parse_html
import os, re, json, csv, random
from urllib.parse import urljoin
from typing import List, Optional
import requests

class ScrapedDocument(BaseModel):
    url: str
    title: str
    content: List[str]  # List of extracted text content

class RufusClient:
    def __init__(self):
        self.nlp = load_nlp_model()
        self.rate_limit = 5  # Time in seconds to wait between requests to avoid rate-limiting

    def _analyze_prompt(self, instructions):
        """
        Analyze the user's instructions using spaCy to extract important keywords dynamically.
        """
        doc = self.nlp(instructions)
        keywords = [token.text for token in doc if token.pos_ in ['NOUN', 'PROPN', 'VERB']]
        return keywords

    async def scrape(self, url, instructions, output_format="json"):
        """
        Main method to scrape data from any website, dynamically extracting content based on the user's prompt.
        Optionally, it can follow links to nested pages using async and scrape relevant content based on extracted keywords.
        Synthesizes content into a structured document format ready for RAG systems.
        """
        try:
            async with async_playwright() as p:
                # Launch the browser
                browser = await p.chromium.launch(headless=True)

                # Create a new browser context with a custom user agent
                context = await browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

                # Open a new page in this context
                page = await context.new_page()
                
                # Go to the page
                await page.goto(url)
                
                # Wait for the content to load
                await page.wait_for_timeout(5000)

                # Extract the page's content
                content = await page.content()
                soup = parse_html(content)

                # Analyze the user's prompt to extract keywords
                query = self._analyze_prompt(instructions)
                print(f"Extracting based on query: {query}")

                # Extract the page's title
                page_title = await page.title()

                # Process the content dynamically based on the prompt keywords
                extracted_data = self._process_content(soup, query)

                # Optionally, follow links to nested pages
                nested_data = await self._follow_links(soup, url, query)
                extracted_data.extend(nested_data)

                await browser.close()

                # Create a structured document for RAG systems
                document = self._synthesize_document(url, page_title, extracted_data, output_format)

                return document

        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None

    def _process_content(self, soup, query):
        """
        Dynamically extract content from a webpage based on keywords from the query.
        This function selectively extracts content based on the dynamically extracted keywords.
        """
        data = []
        
        # Iterate over common HTML elements that may contain relevant content
        for tag in soup.find_all(['p', 'h1', 'h2', 'h3', 'span', 'div', 'li', 'table', 'td', 'form', 'input']):
            text = tag.get_text().strip().lower()
            
            # Match any relevant keyword from the user query to dynamically select content
            if any(keyword.lower() in text for keyword in query):
                data.append(tag.get_text().strip())
        
        return data

    async def _follow_links(self, soup, base_url, query, max_links=5):
        """
        Follow and scrape links to nested pages, if any, asynchronously. This will dynamically extract relevant data based on query keywords from nested pages.
        """
        nested_data = []
        links = soup.find_all('a', href=True)
        followed_links = 0

        for link in links:
            if followed_links >= max_links:
                break
            
            # Resolve relative links
            nested_url = urljoin(base_url, link['href'])

            # Fetch the nested page content asynchronously
            try:
                # Introduce rate limiting between requests
                await asyncio.sleep(self.rate_limit)

                response = requests.get(nested_url)
                response.raise_for_status()
                nested_soup = BeautifulSoup(response.text, 'html.parser')

                # Process content from the nested page
                nested_data.append(f"Link: {nested_url}")
                nested_data.extend(self._process_content(nested_soup, query))
                followed_links += 1

            except requests.RequestException as e:
                print(f"Failed to fetch nested page: {nested_url}. Error: {e}")
        
        return nested_data

    def _synthesize_document(self, url, title, content, output_format="json"):
        """
        Synthesize the extracted content into a structured document format (e.g., JSON or plain text),
        ready for use in RAG systems.
        """
        if output_format == "json":
            return self._save_json(ScrapedDocument(url=url, title=title, content=content))
        elif output_format == "text":
            return self._save_plain_text(ScrapedDocument(url=url, title=title, content=content))
        else:
            raise ValueError(f"Unsupported output format: {output_format}")

    def _save_json(self, document: ScrapedDocument):
        """
        Save the synthesized document in JSON format for use in RAG systems.
        """
        output_dir = "extracted_data"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Generate a sanitized filename from the URL
        sanitized_url = re.sub(r'https?://', '', document.url)
        sanitized_url = re.sub(r'[^\w\-]', '_', sanitized_url)

        json_filename = f"scraped_data_{sanitized_url}.json"
        json_filepath = os.path.join(output_dir, json_filename)
        
        # Save the data as JSON
        with open(json_filepath, 'w') as json_file:
            json.dump(document.dict(), json_file, indent=4)
        
        return f"Data saved to {json_filepath}"

    def _save_plain_text(self, document: ScrapedDocument):
        """
        Save the synthesized document in plain text format, organizing content in a readable manner.
        """
        output_dir = "extracted_data"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Generate a sanitized filename from the URL
        sanitized_url = re.sub(r'https?://', '', document.url)
        sanitized_url = re.sub(r'[^\w\-]', '_', sanitized_url)

        text_filename = f"scraped_data_{sanitized_url}.txt"
        text_filepath = os.path.join(output_dir, text_filename)
        
        # Save the data as plain text
        with open(text_filepath, 'w') as text_file:
            text_file.write(f"URL: {document.url}\n")
            text_file.write(f"Title: {document.title}\n")
            text_file.write("Content:\n")
            text_file.write("\n".join(document.content))
        
        return f"Data saved to {text_filepath}"
