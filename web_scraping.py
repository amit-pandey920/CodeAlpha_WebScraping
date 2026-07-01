import requests
from bs4 import BeautifulSoup
import pandas as pd

# Website URL
url = "https://books.toscrape.com/"

print("=" * 50)
print("        BOOKS TO SCRAPE - WEB SCRAPING")
print("=" * 50)
print("Connecting to the website...\n")

try:
    # Send request to the website
    response = requests.get(url)
    response.raise_for_status()

    # Parse HTML content
    soup = BeautifulSoup(response.text, "html.parser")

    # List to store all book details
    books = []

    # Dictionary to convert rating into stars (for display)
    rating_stars = {
        1: "⭐",
        2: "⭐⭐",
        3: "⭐⭐⭐",
        4: "⭐⭐⭐⭐",
        5: "⭐⭐⭐⭐⭐"
    }

    # Dictionary to convert text rating into numbers (for CSV)
    rating_numbers = {
        "One": 1,
        "Two": 2,
        "Three": 3,
        "Four": 4,
        "Five": 5
    }

    # Find all books on the page
    all_books = soup.find_all("article", class_="product_pod")

    # Extract information from each book
    for book in all_books:

        # Book Title
        title = book.h3.a["title"]

        # Book Price (Remove £ symbol)
        price = book.find("p", class_="price_color").text
        price = price.replace("Â£", "").replace("£", "")
        price = float(price)

        # Book Rating
        rating_text = book.p["class"][1]
        rating_number = rating_numbers[rating_text]

        # Availability
        availability = book.find(
            "p",
            class_="instock availability"
        ).text.strip()

        # Store data for CSV
        books.append({
            "Title": title,
            "Price (£)": price,
            "Rating": rating_number,
            "Availability": availability
        })

    # Create DataFrame
    df = pd.DataFrame(books)

    # Save CSV
    df.to_csv("books_data.csv", index=False)

    print("✅ Web Scraping Completed Successfully!\n")
    print(f"📚 Total Books Scraped : {len(df)}\n")

    print("-" * 95)
    print(f"{'Book Title':45} {'Price':>8} {'Rating':>10} {'Availability':>18}")
    print("-" * 95)

    # Display first 5 books
    for i in range(5):
        print(
            f"{df.iloc[i]['Title'][:45]:45} "
            f"{df.iloc[i]['Price (£)']:>8.2f} "
            f"{rating_stars[df.iloc[i]['Rating']]:>10} "
            f"{df.iloc[i]['Availability']:>18}"
        )

    print("-" * 95)
    print("\n📄 Data saved successfully as 'books_data.csv'")

except requests.exceptions.RequestException as e:
    print("❌ Error connecting to the website.")
    print(e)