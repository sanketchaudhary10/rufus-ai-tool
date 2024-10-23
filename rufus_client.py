import spacy
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from pydantic import BaseModel
from typing import List
import csv
import json
import os
import re

class ScrapedDocument(BaseModel):
    url: str
    data: List[str]

class RufusClient:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")

    def _analyze_prompt(self, instructions):
        """
        Analyze the user's instructions using spaCy to extract important keywords.
        """
        doc = self.nlp(instructions)
        keywords = [token.text for token in doc if token.pos_ in ['NOUN', 'PROPN', 'VERB']]
        return keywords

    def scrape(self, url, instructions, output_format="json"):
        """
        Main method to scrape data from the website and output in the specified format (JSON or CSV).
        """
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                page.goto(url)
                page.wait_for_selector('body')
                content = page.content()
                soup = BeautifulSoup(content, 'html.parser')
                
                # Analyze the prompt to extract keywords
                query = self._analyze_prompt(instructions)
                print(f"Extracting based on query: {query}")
                
                # Process the content and extract data
                extracted_data = self._process_content(soup, query)
                browser.close()

                # Create a structured document
                document = ScrapedDocument(url=url, data=extracted_data)

                # Output format options
                if output_format == "json":
                    return self._save_json(document)
                elif output_format == "csv":
                    return self._convert_to_csv(document)
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None

    def _process_content(self, soup, query):
        """
        Extract relevant content from the webpage based on the query keywords.
        """
        data = []
        for tag in soup.find_all(['p', 'h1', 'h2', 'a', 'div', 'span']):
            text = tag.get_text().lower()
            for keyword in query:
                if keyword.lower() in text:
                    data.append(tag.get_text().strip())
        return data

    def _save_json(self, document):
        """
        Save the scraped data as a JSON file in the project directory, ensuring a valid filename.
        """

        output_dir = "extracted_data"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        # Extract domain name and path from URL to create a cleaner filename
        url = document.url
        sanitized_url = re.sub(r'https?://', '', url)  # Remove 'http://' or 'https://'
        sanitized_url = re.sub(r'[^\w\-]', '_', sanitized_url)  # Replace non-alphanumeric characters with '_'

        # Ensure the filename ends with .json
        json_filename = f"scraped_data_{sanitized_url}.json"
        
        # Get the absolute path to save the JSON file in the current directory
        json_filepath = os.path.join(output_dir, json_filename)
        
        # Save the data as a JSON file
        with open(json_filepath, 'w') as json_file:
            json.dump(document.dict(), json_file, indent=4)
        
        return f"Data saved to {json_filepath}"

    def _convert_to_csv(self, document):
        """
        Convert the scraped data to a CSV file and save it.
        """
        # Creating the file name from the URL
        csv_file = f"scraped_data_{document.url.replace('https://', '').replace('/', '_')}.csv"
        
        # Write the data to CSV
        with open(csv_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["url", "data"])
            for row in document.data:
                writer.writerow([document.url, row])
        
        return f"Data saved to {csv_file}"
