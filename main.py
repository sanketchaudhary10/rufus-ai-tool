from rufus_client import RufusClient

def main():
    # Create a RufusClient instance
    client = RufusClient()

    # Define a real test URL and dynamic instructions
    url = "https://en.wikipedia.org/wiki/Web_scraping"
    instructions = "Extract information about the legality of web scraping."

    # Scrape the website and save the data as a JSON file
    output = client.scrape(url, instructions, output_format="json")
    print(output)

if __name__ == "__main__":
    main()
