import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import time

BASE_URL = "https://books.toscrape.com/catalogue/page-{}.html"


def clean_price(price_text):
    """
    Extract numeric price safely from messy strings like 'Â£51.77'
    """
    match = re.findall(r"\d+\.\d+", price_text)
    return float(match[0]) if match else None


def scrape_page(url):
    try:
        response = requests.get(url, timeout=10)
        response.encoding = "utf-8"
        soup = BeautifulSoup(response.text, "html.parser")

        titles = soup.find_all("h3")
        prices = soup.find_all("p", class_="price_color")

        books = []

        for title, price in zip(titles, prices):
            books.append({
                "title": title.a["title"],
                "price": clean_price(price.text)
            })

        return books

    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return []


def main():
    all_books = []

    # Page 1
    print("Scraping page 1...")
    all_books.extend(scrape_page("https://books.toscrape.com/"))

    # Pages 2–50
    for page in range(2, 51):
        url = BASE_URL.format(page)
        print(f"Scraping page {page}...")

        all_books.extend(scrape_page(url))

        time.sleep(0.5)  # polite scraping

    # Convert to DataFrame
    df = pd.DataFrame(all_books)

    # -------------------------
    # 📊 BASIC STATISTICS
    # -------------------------
    stats = {
        "mean_price": df["price"].mean(),
        "min_price": df["price"].min(),
        "max_price": df["price"].max(),
        "total_books": len(df)
    }

    stats_df = pd.DataFrame([stats])

    print("\n📊 Price Statistics:")
    print(stats_df)

    # -------------------------
    # 💾 SAVE FILES
    # -------------------------
    df.to_csv("books.csv", index=False)
    df.to_excel("books_data.xlsx", index=False)
    stats_df.to_excel("summary.xlsx", index=False)

    print("\n✅ Data saved successfully!")


if __name__ == "__main__":
    main()