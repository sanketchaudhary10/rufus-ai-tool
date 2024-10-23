from rufus_client import RufusClient
from rufus_api import RufusAPI
import os
from dotenv import load_dotenv
import asyncio

# Load environment variables from the .env file
load_dotenv()

# Access the environment variables
api_key = os.getenv('RUFUS_API_KEY')

# Initialize the Rufus API with the key
client = RufusAPI(api_key=api_key)

# Instructions for scraping
instructions = "Find Learn how to apply for Graduate Students"

# Scrape data from the URL asynchronously
async def main():
    documents = await client.scrape("https://admissions.indiana.edu/apply/index.html", instructions)
    print(documents)

# Ensure to run this in an async context
if __name__ == "__main__":
    asyncio.run(main())

