import asyncio
from playwright.async_api import async_playwright
import re

async def get_sum(page, url):
    total = 0
    await page.goto(url, timeout=60000)
    await page.wait_for_selector("table")

    while True:
        await page.wait_for_selector("table td")
        cells = await page.locator("table td").all_inner_texts()

        for cell in cells:
            numbers = re.findall(r"-?\d+", cell)
            for num in numbers:
                total += int(num)

        next_button = page.locator("a.paginate_button.next")

        if await next_button.count() > 0:
            classes = await next_button.get_attribute("class")
            if classes and "disabled" not in classes:
                await next_button.click()
                await page.wait_for_timeout(500)
            else:
                break
        else:
            break

    return total


async def main():
    seeds = range(84, 94)
    grand_total = 0

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        for seed in seeds:
            url = f"https://sanand0.github.io/tdsdata/js_table/?seed={seed}"
            s = await get_sum(page, url)
            print(f"Seed {seed}: {s}")
            grand_total += s

        await browser.close()

    print("FINAL TOTAL:", grand_total)


if __name__ == "__main__":
    asyncio.run(main())