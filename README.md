# Rufus AI Agent Documentation

## Project Overview
Rufus is an AI web-scraping agent designed to dynamically extract data from websites based on user-defined prompts and output it in structured formats for RAG (Retrieval-Augmented Generation) pipelines.

**Core Features**:
- Asynchronous web scraping to handle multiple tasks concurrently.
- Dynamic content extraction based on the user’s prompt.
- Supports crawling nested pages for deep scraping.
- Synthesizes output into structured formats like JSON and plain text, ready for use in RAG pipelines.

## How Rufus Works

1. **Initialize Rufus API**: The `RufusAPI` class is initialized with an optional API key for handling authenticated requests.
2. **Analyze User Instructions**: Based on the provided prompt, Rufus analyzes the instructions using an NLP model (via spaCy) to extract keywords.
3. **Scraping Content**: Rufus scrapes the website by visiting the URL extracting content, and following nested links if required.
4. **Process and Synthesize Data**: Extracted content is processed and organized into a structured document.
5. **Output for RAG Pipelines**: The data is ready to be used in RAG pipelines making it easier to integrate into LLM or chatbot systems.

### Steps to Use Rufus

**1. Installation**:
Install Rufus and its dependencies using the following commands:

## Cloning the Repository
```bash
git clone https://github.com/sanketchaudhary10/rufus-ai-tool.git
cd rufus-ai-tool
```

## Installing the required libraries
```bash
pip install -r requirements.txt
playwright install
```

## Creating an Environment Variables file
```bash
## Create a .env file in the root directory to store your API key:
touch .env

## Add the following line to your .env file:
RUFUS_API_KEY=your_api_key_here
```

## Usage

Here's an example to demonstrate how to use Rufus to scrape a website:

## Below is the main.py file that can be used to run the Rufus AI Agent

```python
from rufus_api import RufusAPI
import os
from dotenv import load_dotenv
import asyncio

# Load environment variables
load_dotenv()
api_key = os.getenv('RUFUS_API_KEY')

# Initialize RufusAPI
client = RufusAPI(api_key=api_key)

# Instructions for scraping
instructions = "Extract application information for graduate students."

async def main():
    documents = await client.scrape("https://admissions.indiana.edu/apply/index.html", instructions)
    print(documents)

asyncio.run(main())
```

## Integrating Rufus into a RAG Pipeline

Rufus can easily integrate into any RAG pipeline by feeding the scraped data directly into the system. Steps on implementing Rufus into an example RAG Model System:

### Example Integration
Below is an example of how to use Rufus within a RAG system:

```python
from your_llm_model import RAGModel  # Example LLM model for your RAG pipeline
from rufus_api import RufusAPI
import asyncio

# Initialize Rufus and RAG system
client = RufusAPI(api_key='your_api_key')
rag_model = RAGModel()

# Instructions for scraping
instructions = "Extract FAQs for customer support."

async def integrate_rufus_into_rag():
    documents = await client.scrape("https://example.com/faqs", instructions)
    rag_model.add_documents(documents.content)  # Add scraped content to RAG model

asyncio.run(integrate_rufus_into_rag())
```

## Some of the Example Use Cases that Rufus can solve (Scrape):
- Chatbot FAQs: Scrape FAQ data from websites and feed it into chatbots.
- Price Comparisons: Scrape product prices and features for financial comparison models.
- Application Data: Extract application processes from university or job websites.

## Error Handling
Rufus implements basic error handling for cases where the web page is inaccessible, where rate-limiting is triggered, or where the content format changes unexpectedly.

```python
try:
    documents = await client.scrape("https://broken-link.com", instructions)
except Exception as e:
    print(f"An error occurred: {e}")
```

## API Reference
## RufusClient Class:
```python
class RufusClient:
    def __init__(self, api_key: str):
        # Initializes RufusClient with API key

    async def scrape(self, url: str, instructions: str, output_format: str = "json"):
        # Scrapes data from the given URL based on the instructions
```

## RufusAPI Class:
```python
class RufusAPI:
    def __init__(self, api_key: str):
        # Initializes the RufusAPI

    async def scrape(self, url: str, instructions: str, output_format: str = "json"):
        # Scrape data asynchronously from the provided URL
```