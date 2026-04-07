import requests
from bs4 import BeautifulSoup as bsp
import csv


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0"
    }
base_url = "https://books.toscrape.com/"
run = False
try :
    response = requests.get("https://books.toscrape.com",headers = headers, timeout = 10)
    response.raise_for_status()
    soup = bsp(response.text, "html.parser")

    ol = soup.find("ol", class_ = "row")
    books_a = ol.select("li.col-xs-6.col-sm-4.col-md-3.col-lg-3 article.product_pod h3 a")
    run = True
except requests.exceptions.Timeout:
    print("Time Out")
    print("Can't reach the site ")

except requests.exceptions.ConnectionError:
    print("Internet is off")

except requests.exceptions.HTTPError as e :
    print(f"Error :{e}")


n = 0
total = 0

with open ("BookScrap.csv", "w", newline = "", encoding = "utf-8") as file:
    fieldnames = ["title", "price"]
    writer = csv.DictWriter(file, fieldnames = fieldnames)
    writer.writeheader()
    if run:
        try:
            for a in books_a:
                link = a['href']
                book_link = base_url + link
                response_book = requests.get(book_link, headers = headers, timeout = 10)
                response_book.raise_for_status()


                soup_book = bsp(response_book.text, "html.parser")
                book_name = soup_book.select_one("div.col-sm-6.product_main h1")
                book_price_ = soup_book.select_one("div.col-sm-6.product_main p.price_color")
                book_name = book_name.text
                book_price = book_price_.text
                book_price = book_price.replace("Â", "")
                n = n+1

                csv_file = {'title': book_name, 'price': book_price}
                writer.writerow(csv_file)

                print(f"{n}. Book name : {book_name}")
                print(f"{book_name} price : {book_price}")
                currency, price = book_price.split("£")
                total = total + float(price)

            print(f"Total Books are {n}")
            print(f"Total price of {n} books is {total}")

        except requests.exceptions.Timeout:
            print("Time Out")
            print("Can't reach the site ")

        except requests.exceptions.ConnectionError:
            print("Internet is off")

        except requests.exceptions.HTTPError as e :
            print(f"Error of {book_name} : {e}")


