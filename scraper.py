from bs4 import BeautifulSoup
import requests 
import pandas as pd


data = []
#  multi page scraping
for i in range(5):
    #   url to scrape from 
    URL = f"https://books.toscrape.com/catalogue/page-{i}.html"

    # make a http resquest to load the page
    response = requests.get(url=URL)

    # pare the page with beautifulsoup
    b_soup = BeautifulSoup(response.text, features= "html.parser")

    # extract the books 
    books  = b_soup.find_all(name="article", class_="product_pod")

    # loop through the books and extract their title, price and ratings
    for book in books:
        title = book.h3.a["title"] #type:ignore

        price = book.find(name="p", class_="price_color").text #type:ignore

        rating  = book.p["class"][0] #type:ignore

        # save in a list of dicts the extracted fields
        data.append({
            "title":title,
            "price":price,
            "rating":rating
        })

    # create a dataframe with the the data
    df = pd.DataFrame(data)

    # save the dataframe to a csv file
    df.to_csv("product.csv", index=False)


    print(f"Scraping of page {i} completed!")

print("Scraping done ✅")