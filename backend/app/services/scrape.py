import asyncio
from playwright.async_api import async_playwright

async def scrape_closures():
  """
  Scrapes the Orange County restaurant closures and prints the data to the console.
  """
  url = "https://inspections.myhealthdepartment.com/orange-county/restaurant-closures"
  
  async with async_playwright() as p:
    print(f"Launching browser and navigating to: {url}")
    browser = await p.chromium.launch(headless=True)
    # Create a context with a real User-Agent to avoid bot detection
    context = await browser.new_context(
      user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    )
    page = await context.new_page()
    
    await page.goto(url)
    
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
          scraped_data.append(row_data)
          print(f"Scraped Row: {row_data}")
        
    except Exception as e:
      print(f"Error encountered while scraping: {e}")
    finally:
      await browser.close()

if __name__ == "__main__":
  asyncio.run(scrape_closures())