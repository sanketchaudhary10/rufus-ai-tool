import spacy
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from pydantic import BaseModel
from utils.nlp_utils import load_nlp_model
from utils.scraping_utils import parse_html
from transformers import pipeline
import os, re, json, csv, time, random, requests
from urllib.parse import urljoin
from typing import List



class ScrapedDocument(BaseModel):
    url: str
    data: List[str]

class RufusClient:
    def __init__(self):
        self.nlp = load_nlp_model()

    def _analyze_prompt(self, instructions):
        """
        Analyze the user's instructions using spaCy to extract important keywords.
        """
        doc = self.nlp(instructions)
        keywords = [token.text for token in doc if token.pos_ in ['NOUN', 'PROPN', 'VERB']]
        return keywords

    def scrape(self, url, instructions, output_format="json"):
        """
        Main method to scrape data from any website, dynamically extracting content based on the user's prompt.
        Optionally, it can follow links to nested pages.
        """
        try:
            with sync_playwright() as p:
                # Launch the browser
                browser = p.chromium.launch(headless=True)

                # Create a new browser context with a custom user agent
                context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

                # Open a new page in this context
                page = context.new_page()
                
                # Go to the page
                page.goto(url)
                
                # Wait for the content to load
                page.wait_for_timeout(5000)

                # Extract the page's content
                content = page.content()
                soup = parse_html(content)

                # Analyze the user's prompt to extract keywords
                query = self._analyze_prompt(instructions)
                print(f"Extracting based on query: {query}")

                # Process the content dynamically based on the prompt keywords
                extracted_data = self._process_content(soup, query)

                # Optionally, follow links to nested pages
                nested_data = self._follow_links(soup, url, query)
                extracted_data.extend(nested_data)

                browser.close()

                # Create a structured document
                document = ScrapedDocument(url=url, data=extracted_data)

                # Output format (JSON or CSV)
                if output_format == "json":
                    return self._save_json(document)
                elif output_format == "csv":
                    return self._convert_to_csv(document)

        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None


    def _process_content(self, soup, query):
        """
        Dynamically extract content from a webpage based on keywords from the query.
        It will search through paragraphs, headings, tables, and lists without any hardcoded logic for specific types of content.
        """
        data = []
        
        # Iterate over common HTML elements that may contain relevant content
        for tag in soup.find_all(['p', 'h1', 'h2', 'h3', 'span', 'div', 'li', 'table', 'td']):
            text = tag.get_text().strip().lower()
            
            # Match any relevant keyword from the user query to dynamically select content
            if any(keyword.lower() in text for keyword in query):
                data.append(tag.get_text().strip())
        
        return data


    

    def _follow_links(self, soup, base_url, query, max_links=5):
        """
        Follow and scrape links to nested pages, if any. This allows the agent to gather more content from multi-page websites.
        Add rate limiting and limit the number of links followed.
        """
        nested_data = []
        links = soup.find_all('a', href=True)
        followed_links = 0

        for link in links:
            # Only follow a limited number of links to avoid overwhelming the server
            if followed_links >= max_links:
                break
            
            # Resolve relative links
            nested_url = urljoin(base_url, link['href'])

            # Fetch the nested page content with error handling and random delays
            try:
                # Introduce a delay between requests to avoid rate-limiting
                time.sleep(random.uniform(3, 6))

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
