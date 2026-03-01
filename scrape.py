"""Scrape 10 table pages and sum all values."""

import asyncio
from playwright.async_api import async_playwright

SEEDS = [84, 85, 86, 87, 88, 89, 90, 91, 92, 93]
BASE_URL = "https://sanand0.github.io/tdsdata/js_table/?seed="


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        grand_total = 0

        for seed in SEEDS:
            page = await browser.new_page()
            url = f"{BASE_URL}{seed}"

            await page.goto(url, wait_until="networkidle")
            await page.wait_for_selector("table")

            cells = await page.query_selector_all("table td")
            page_sum = 0

            for cell in cells:
                text = await cell.inner_text()
                try:
                    page_sum += int(text.strip())
                except ValueError:
                    pass

            print(f"Seed {seed}: sum = {page_sum}")
            grand_total += page_sum
            await page.close()

        await browser.close()
        print(f"\nGRAND TOTAL: {grand_total}")


if __name__ == "__main__":
    asyncio.run(main())