from bs4 import BeautifulSoup
import requests 
from requests.exceptions import RequestException
from utils import save_to_csv, save_to_json

BASE_URL = "https://books.toscrape.com/catalogue/page-{}.html"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}


def scrape_and_save(url_path:str,num_pages:int, save_method:str="to_json"):
    """
    Scare data from an online store then save to json or csv
    Args:
        url_path: link to the website to scrape from
        num_pages: number of pages to be scraped
        save_method: to_json or to_csv save the data either as a CSV file, a JSON 
    """
    storage:list = []

    for page in range(1,num_pages + 1 ):
    
        url = url_path.format(page)

        try:
            # make a http resquest to load the page
            response = requests.get(url=url, headers=HEADERS, timeout=10)
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
                storage.append({
                    "title":title,
                    "price":price,
                    "rating":rating
                })  
            print(f"page {page} sucessfully scraped ✅✅✅")

        except RequestException as e:
            print(f"URL {url} is not working, failed to scrape page:{page} ❌❌❌ \nREASON:{e}")
            return False
        
    if save_method.lower() == "to_csv":
        # save the data to a csv file
        save_to_csv(data=storage, filename="output/books.csv")
    elif save_method.lower() == "to_json":
        # save the dataframe to json file
        save_to_json(data=storage, filename="output/books.json")
    else:
        # save both if no prefered format is choosen 
        save_to_csv(data=storage, filename="output/books.csv")
        save_to_json(data=storage, filename="output/books.json")

    print("Scraping completed ℹ️ℹ️ℹ️ ")
    
scrape_and_save(url_path=BASE_URL,num_pages=1, save_method="to_json" )
