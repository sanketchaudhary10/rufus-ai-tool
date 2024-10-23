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
instructions = "Find price of Dan Brown Books on Amazon"

# Scrape data from the URL asynchronously
async def main():
    documents = await client.scrape("https://www.amazon.com/s?k=dan+brown&crid=3MMLLV3NUI1ZH&sprefix=dan+brown%2Caps%2C133&ref=nb_sb_noss_1", instructions)
    print(documents)

# Ensure to run this in an async context
if __name__ == "__main__":
    asyncio.run(main())

