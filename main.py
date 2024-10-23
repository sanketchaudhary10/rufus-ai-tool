from rufus_client import RufusClient
import asyncio

async def main():
    # Create a RufusClient instance
    client = RufusClient()

    # Define a real test URL and dynamic instructions
    url = "https://admissions.indiana.edu/apply/learn-more-faq.html"
    instructions = "Find the FAQs related to admission"

    # Scrape the website and save the data as a JSON file
    output = await client.scrape(url, instructions, output_format="json")
    print(output)

if __name__ == "__main__":
    asyncio.run(main())


