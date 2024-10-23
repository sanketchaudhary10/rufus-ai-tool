from rufus_client import RufusClient

class RufusAPI:
    def __init__(self):
        self.client = RufusClient()

    def scrape(self, url, instructions):
        return self.client.scrape(url, instructions)
