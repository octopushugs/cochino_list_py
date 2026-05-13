from datetime import datetime

from .scrape import ScrapeService
from .populate import PopulateService

class ScrapeAndPopulateService:
  def __init__(self):
    # No direct DB session in constructor, as the job manages its own.
    # This makes the service more flexible and suitable for background tasks
    # where a session might not be available or needs to be created per execution.
    pass

  async def populate_closures_job(self):
    """
    Background job to scrape closure data and populate the database.
    """    
    print(f"Executing daily scrape and populate job at {datetime.now()}")
    print("Starting data scraping...")

    scrape_service = ScrapeService()
    scraped_data = await scrape_service.scrape_closures()
    print(f"Finished scraping. Found {len(scraped_data)} records.")

    if scraped_data:
      print("Starting database population...")
      populate_service = PopulateService()
      populate_service.populate_records(scraped_data)
      print("Finished database population.")
    else:
      print("No data scraped, skipping database population.")

# Allows the script to be run directly from the command line for manual scraping and population
if __name__ == "__main__":
    import asyncio
    service = ScrapeAndPopulateService()
    asyncio.run(service.populate_closures_job())