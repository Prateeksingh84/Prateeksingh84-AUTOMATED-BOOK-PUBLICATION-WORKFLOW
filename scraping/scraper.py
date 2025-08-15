# src/scraping/scraper.py

import os
import asyncio
import re
from playwright.async_api import async_playwright

def _sanitize_title(title: str) -> str:
    """
    Sanitizes a string to be a valid filename.
    Replaces invalid characters and trims whitespace.
    """
    safe_title = re.sub(r'[\\/:*?"<>|]', '_', title)
    safe_title = safe_title.replace(' ', '_')
    safe_title = safe_title.strip('_.')
    return safe_title

async def scrape_chapter(url: str, output_dir: str = "data") -> tuple[str, str] | None:
    """
    Navigates to a given URL, scrapes the main chapter content, saves it
    to a text file, and takes a full-page screenshot.

    Args:
        url (str): The URL of the web page to scrape.
        output_dir (str): The directory where the scraped content and screenshots will be saved.

    Returns:
        tuple[str, str] | None: A tuple containing (text_file_path, screenshot_path) if successful, otherwise None.
    """
    print(f"Starting to scrape: {url}")
    
    os.makedirs(output_dir, exist_ok=True)

    async with async_playwright() as playwright:
        browser = None
        try:
            # Launch a headless browser
            # Change headless=True to headless=False temporarily for visual debugging if needed
            browser = await playwright.chromium.launch(headless=True) 
            page = await browser.new_page()

            print(f"DEBUG: Navigating to page: {url}")
            await page.goto(url, wait_until='domcontentloaded')
            print("DEBUG: Page loaded successfully.")

            chapter_title_element = await page.query_selector('h1')
            chapter_title = await chapter_title_element.inner_text() if chapter_title_element else "Untitled Chapter"
            print(f"DEBUG: Captured title: {chapter_title}")

            content_selector = "#mw-content-text"
            content_element = await page.query_selector(content_selector)

            if not content_element:
                print("Error: Could not find main content element. Selector might be wrong or content not loaded.")
                return None
            
            content_html = await content_element.inner_html()
            original_text = re.sub('<[^<]+?>', '', content_html)
            chapter_content = re.sub(r'\n\s*\n', '\n\n', original_text).strip()
            
            safe_title = _sanitize_title(chapter_title)
            text_path = os.path.join(output_dir, f"{safe_title}.txt")

            with open(text_path, "w", encoding="utf-8") as f:
                f.write(chapter_content)
            print(f"DEBUG: Content saved to {text_path}")
                
            screenshot_path = os.path.join(output_dir, f"{safe_title}_screenshot.png")
            await page.screenshot(path=screenshot_path, full_page=True)
            print(f"DEBUG: Screenshot saved to {screenshot_path}")
            
            print(f"Scraped '{chapter_title}' and saved to {text_path}")
            print(f"Screenshot saved to {screenshot_path}")
            
            # Return both the text file path and the screenshot path
            return text_path, screenshot_path 
            
        except Exception as e:
            print(f"AN UNEXPECTED ERROR OCCURRED DURING SCRAPING: {e}")
            return None
        finally:
            if browser:
                await browser.close()
            print("DEBUG: Browser closed.")

# Example usage (for testing purposes)
if __name__ == "__main__":
    async def main():
        url = "https://en.wikisource.org/wiki/The_Gates_of_Morning/Book_1/Chapter_1"
        scraped_result = await scrape_chapter(url, output_dir=os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')) 
        if scraped_result:
            text_file, screenshot_file = scraped_result
            with open(text_file, "r", encoding="utf-8") as f:
                print("\n--- Scraped Content ---")
                print(f.read()[:500])
            print(f"Screenshot path: {screenshot_file}")
        else:
            print("\nScraping failed.")

    asyncio.run(main())
