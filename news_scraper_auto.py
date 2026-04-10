import requests
from bs4 import BeautifulSoup as bsp
import csv
import time
import random

class NewsDetail:
    def __init__ (self, link):

        self.fieldnames = ['S.No.', 'Title', 'Date and Time', 'Link']
        if "https://timesofindia.indiatimes.com" not in link:
            url = "https://timesofindia.indiatimes.com"+link
            print(url)
        else :
            url = link

        response = link_opner(url)

        if response is None:
            self.title = "N/A"
            self.date_time = "N/A"
            self.link = link
            return


        soup = bsp(response.text, 'html.parser')


        title = soup.select_one("h1.cMyCH span")
        title = title.text if title else "N/A"
        date_time =soup.select_one("div.Kx85U.innerbody div.AhY1R div.inl71 div.HRita.byline_action div.Lf73Q.byline span")
        date_time = date_time.text if date_time else "N/A"


        self.link = link
        self.title = title
        self.date_time = date_time





    def csv_save(self):
        try:
            with open("news_scraper_auto_details.csv", 'r', newline='', encoding='utf-8-sig') as f:
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
                    with open("news_scraper_auto_details.csv", 'a', newline='', encoding='utf-8-sig') as file:
                        writer = csv.DictWriter(file, fieldnames = self.fieldnames)
                        csv_file = {'S.No.': serial_number, 'Title' : self.title, 'Date and Time' : self.date_time, 'Link': self.link}
                        writer.writerow(csv_file)


        except FileNotFoundError:
            with open("news_scraper_auto_details.csv", 'a', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames = self.fieldnames)
                writer.writeheader()
                csv_file = {'S.No.': 1, 'Title' : self.title, 'Date and Time' : self.date_time, 'Link': self.link}

                writer.writerow(csv_file)




def link_opner(url):

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0"
            }

        response = requests.get(url, headers = headers , timeout = 10)
        response.raise_for_status()
        return response

    except requests.exceptions.Timeout:
        print("Time Out")
        print("Can't reach the site ")
        return None

    except requests.exceptions.ConnectionError:
        print("Internet is off")
        return None
    except requests.exceptions.HTTPError as e :
        print(f"Error : {e}")
        return None




url = "https://timesofindia.indiatimes.com/technology"


response = link_opner(url)

soup = bsp(response.text, 'html.parser')


#yeh complete_page pure page ka data rakhta hai
complete_page = soup.select_one("div.Qxxtu ")

all_links = set()
all_links = complete_page.select("a")

n = 0
# targeted_tags = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'span']
for link in all_links :
    link = link['href']
    if "articleshow" in link:
        n +=1
        print(n)
        proccess = NewsDetail(link)
        proccess.csv_save()
        time_sleep = random.uniform(0.5, 1)
        time.sleep(time_sleep)

