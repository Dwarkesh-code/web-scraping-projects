import requests
from bs4 import BeautifulSoup as bsp
import csv
import time
import random

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0"
    }

url = "https://quotes.toscrape.com"
n = 1
i = 0

with open ("quote_csv.csv", "w", newline = "", encoding = "utf-8") as file :
    fieldnames = ['quotes', 'author']
    writer = csv.DictWriter(file, fieldnames = fieldnames)
    writer.writeheader()

    while True :

        try :

            response = requests.get(url , headers = headers , timeout = 10)
            response.raise_for_status()
            soup = bsp(response.text, "html.parser")
            quote_details = soup.select("div.quote")

            if not quote_details:
                break
            for quote_detail in quote_details :
                quote = quote_detail.select_one("span.text").text
                quote_author = quote_detail.select_one("small.author")
                i = i+1
                print(f"{i}. {quote}")
                print(f"by {quote_author.text} \n \n")
                csv_file = {'quotes': quote, 'author': quote_author.text}
                writer.writerow(csv_file)


            url = "https://quotes.toscrape.com"
            n = n+1
            if n >= 2:
                url = url + f'/page/{n}/'
            time_sleep = random.uniform(1,5)
            print("It taken time something :",time_sleep)
            time.sleep(time_sleep)


        except requests.exceptions.Timeout:
            print("Time Out")
            print("Can't reach the site ")

        except requests.exceptions.ConnectionError:
            print("Internet is off")

        except requests.exceptions.HTTPError as e :
            print(f"Error : {e}")

