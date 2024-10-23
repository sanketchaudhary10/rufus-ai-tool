from rufus_client import RufusClient

def main():
    # Create a RufusClient instance
    client = RufusClient()

    # Define the URL and instructions for scraping
    url = "https://www.amazon.com/s?k=monitors&i=computers&crid=1IRL5W83GYNHI&sprefix=monitors%2Ccomputers%2C124&ref=nb_sb_ss_pltr-data-refreshed_1_8"
    instructions = "Extract details of all the Dell Monitors"

    # Scrape the website and output the data as JSON
    json_data = client.scrape(url, instructions, output_format="json")
    print("JSON Output:", json_data)

    # # Scrape the website and save the data as CSV
    # csv_output = client.scrape(url, instructions, output_format="csv")
    # print(csv_output)

if __name__ == "__main__":
    main()
