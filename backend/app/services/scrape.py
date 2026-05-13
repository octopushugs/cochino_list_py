import asyncio
from playwright.async_api import async_playwright

class ScrapeService:
  def __init__(self):
    self.url = "https://inspections.myhealthdepartment.com/orange-county/restaurant-closures"

  async def scrape_closures(self):
    """
    Scrapes the Orange County restaurant closures and returns the data.
    """
    async with async_playwright() as p:
      print(f"Launching browser and navigating to: {self.url}")
      browser = await p.chromium.launch(headless=True)
      # Create a context with a real User-Agent to avoid bot detection
      context = await browser.new_context(
        user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
      )
      page = await context.new_page()
      
      await page.goto(self.url)
      
      try:
        # Wait specifically for the table element to be visible
        print("Waiting for table to load...")
        await page.wait_for_selector("table", state="visible", timeout=15000)
        
        # Extract all table rows
        rows = await page.query_selector_all("table tr")
        
        scraped_data = []
        
        for row in rows:
          # Find all data cells in the current row
          cells = await row.query_selector_all("td")
          
          if cells:
            # Extract and clean text from each cell into an array
            row_data = [ (await cell.inner_text()).strip() for cell in cells ]
            row_map = {
              "establishment_name": row_data[0],
              "permit_name": row_data[1],
              "address": row_data[2],
              "city": row_data[3],
              "zip": row_data[4],
              "result": row_data[5],
              "closed_on": row_data[6],
              "reason": row_data[7],
              "reopened_on": row_data[8]
            }
            scraped_data.append(row_map)
            print(f"Scraped Row: {row_map}")
          
        return scraped_data

      except Exception as e:
        print(f"Error encountered while scraping: {e}")
        return []
      finally:
        await browser.close()

if __name__ == "__main__":
  service = ScrapeService()
  asyncio.run(service.scrape_closures())