import requests
from bs4 import BeautifulSoup as bsp
import csv
import time
import random

class NewsDetail:
    def __init__ (self, detail, title_tag):
        link = detail.select_one("a")['href']
        catagory = detail.select_one("a div.B7Swb span.mDC_z")
        catagory = catagory.text if catagory else "N/A"
        date = detail.select_one("a div.B7Swb div.TnasD")
        date = date.text if date else "N/A"
        tag = f"a {title_tag}"
        title = detail.select_one(tag)
        title = title.text if title else "N/A"

        self.link = link
        self.catagory = catagory
        self.title = title
        self.date = date
        self.fieldnames = ['S.No.', 'Title', 'Catagory', 'Date', 'Link']



    def csv_save(self):
        try:
            with open("news_scrape_deatails.csv", 'r', newline='', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                reader_list = list(reader)
                old_links = set()
                old_links = {row['Link'] for row in reader_list}


                if reader_list:
                    serial_number = reader_list[-1]
                    serial_number = int(serial_number['S.No.']) +1
                else :
                    serial_number = 1

                if self.link not in old_links:
                    with open("news_scrape_deatails.csv", 'a', newline='', encoding='utf-8-sig') as file:
                        writer = csv.DictWriter(file, fieldnames = self.fieldnames)
                        csv_file = {'S.No.': serial_number, 'Title' : self.title, 'Catagory' : self.catagory, 'Date' : self.date, 'Link': self.link}
                        writer.writerow(csv_file)


        except FileNotFoundError:
            with open("news_scrape_deatails.csv", 'a', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames = self.fieldnames)
                writer.writeheader()
                csv_file = {'S.No.': 1, 'Title' : self.title, 'Catagory' : self.catagory, 'Date' : self.date, 'Link': self.link}

                writer.writerow(csv_file)





url = "https://timesofindia.indiatimes.com/technology"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0"
    }

try:
    response = requests.get(url, headers = headers , timeout = 10)
    response.raise_for_status()
    soup = bsp(response.text, 'html.parser')


    #yeh complete_page pure page ka data rakhta hai
    complete_page = soup.select_one("div.Qxxtu ")

    #yeh jo uper ki top news ka data rakhta hai
    top_news = complete_page.select_one("div.row div.lwmXx div.OFOq0 div.ydXFk")

    first_top_news = top_news.select_one("div.bDDGG div.qWOAq div.tHlTu div.lsufY")

    time_sleep = random.uniform(1,5)
    time.sleep(time_sleep)

    tag = "h5"
    first = NewsDetail(first_top_news, tag)
    first.csv_save()

    time_sleep = random.uniform(1,5)
    time.sleep(time_sleep)

    some_top_news = top_news.select("div.bDDGG div.qWOAq div.i9tIw div.S2wVB div.P5Atq")

    for some_news in some_top_news :

        tag = "h5"
        some = NewsDetail(some_news, tag)
        some.csv_save()

        time_sleep = random.uniform(1,5)
        time.sleep(time_sleep)


except requests.exceptions.Timeout:
    print("Time Out")
    print("Can't reach the site ")

except requests.exceptions.ConnectionError:
    print("Internet is off")

except requests.exceptions.HTTPError as e :
    print(f"Error : {e}")

