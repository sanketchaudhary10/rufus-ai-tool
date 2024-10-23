# Rufus AI Agent Documentation

## Project Overview
Rufus is an AI web-scraping agent designed to dynamically extract data from websites based on user-defined prompts and output it in structured formats for RAG (Retrieval-Augmented Generation) pipelines.
...

**Core Features**:
- Dynamic content extraction based on user-defined prompts.
- Handling of dynamic web content such as JavaScript-rendered pages.
- Ability to follow links and scrape nested pages.
- Output formats (JSON or plain text).

### Steps to Use Rufus

**1. Installation**:
Install Rufus and its dependencies using the following commands:

```bash
git clone https://github.com/yourusername/rufus-ai-agent.git
cd rufus-ai-agent
pip install -r requirements.txt
playwright install

## Cloning the Repository
git clone https://github.com/yourusername/rufus-ai-agent.git
cd rufus-ai-agent

## Create a .env file in the root directory to store your API key:
touch .env

## Add the following line to your .env file:
RUFUS_API_KEY=your_api_key_here

## Usage

Here's a quick example to demonstrate how to use Rufus to scrape a website:

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


## Integrating Rufus into a RAG Pipeline

Rufus can be seamlessly integrated into a Retrieval-Augmented Generation (RAG) pipeline to enhance information retrieval and content generation. Here's how to do it:

### Overview of RAG
A RAG pipeline combines the strengths of retrieval systems and generative models, allowing you to retrieve relevant documents and generate context-aware responses.

### Example Integration
Below is an example of how to use Rufus within a RAG system:

```python
from your_llm_model import RAGModel  # Hypothetical LLM model in your RAG pipeline
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
