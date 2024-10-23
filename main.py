from rufus_client import RufusClient
import asyncio

async def main():
    # Create a RufusClient instance
    client = RufusClient()

    # Define a real test URL and dynamic instructions
    url = "https://jobs.apple.com/en-us/search?location=united-states-USA&team=natural-language-processing-and-speech-technologies-MLAI-NLP"
    instructions = "Find the application form details for the Machine Learning Engineer"

    # Scrape the website and save the data as a JSON file
    output = await client.scrape(url, instructions, output_format="json")
    print(output)

if __name__ == "__main__":
    asyncio.run(main())


