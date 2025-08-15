import asyncio
import os
from playwright.async_api import async_playwright

async def scrape_chapter(url: str, output_dir: str = "data"):
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        try:
            await page.goto(url, wait_until="domcontentloaded")
            
            title_selector = "h1"
            content_selector = "#mw-content-text"
            
            chapter_title = await page.locator(title_selector).inner_text()
            chapter_content = await page.locator(content_selector).inner_text()
            
            safe_title = "".join(c for c in chapter_title if c.isalnum() or c in (' ', '_')).rstrip()
            
            text_path = os.path.join(output_dir, f"{safe_title}.txt")
            with open(text_path, "w", encoding="utf-8") as f:
                f.write(chapter_content)
                
            screenshot_path = os.path.join(output_dir, f"{safe_title}_screenshot.png")
            await page.screenshot(path=screenshot_path, full_page=True)
            
            print(f"Scraped '{chapter_title}' and saved to {text_path}")
            print(f"Screenshot saved to {screenshot_path}")
            
            return chapter_content 
        except Exception as e:
            print(f"An error occurred during scraping: {e}")
            return None
        finally:
            await browser.close()