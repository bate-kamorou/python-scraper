from bs4 import BeautifulSoup
import requests 
from requests.exceptions import RequestException
import pandas as pd

def scrape_and_save(url_path:str, save_method:str="to_json"):
    """
    Scare data from an online store then save to json or csv
    Args:
        url_path: link to the website to scrape from
        save_methode: to_json or to_csv save the data either as a CSV file, a JSON 
    """
    data = []
    
    url = url_path
    try:
        # make a http resquest to load the page
        response = requests.head(url=url, timeout=5)
        response.raise_for_status()  # Raise an exception for bad status codes
        print(f"URL {url} is working (status code: {response.status_code})")
        # pare the page with beautifulsoup
        b_soup = BeautifulSoup(response.text, features= "html.parser")
        # extract the books 
        books  = b_soup.find_all(name="article", class_="product_pod")
        # loop through the books and extract their title, price and ratings
        for  book in books:
            title = book.h3.a["title"] #type:ignore
            price = book.find(name="p", class_="price_color").text #type:ignore
            rating  = book.p["class"][1] #type:ignore
            # save in a list of dicts the extracted fields
            data.append({
                "title":title,
                "price":price,
                "rating":rating
            })

        # create a dataframe with the the data
        df = pd.DataFrame(data)

        if save_method == "to_csv":
            # save the dataframe to a csv file
            df.to_csv("product.csv", index=False)
        else:
            # save the dataframe to json file
            df.to_json("data.json", indent=4)


    except RequestException as e:
        print(f"URL {url} is not working: {str(e)}")
        return False
    


for page in range(1, 4):

    url = f"https://books.toscrape.com/catalogue/page-{page}.html"
    
    if scrape_and_save(url_path=url, save_method="to_csv") != False:
        print(f"Books form page: {page}  are successfully saved ℹ️")
    else:
        print(f"Failed to scrape page: {page} ❌")
  

print("Scraping done ✅✅✅")