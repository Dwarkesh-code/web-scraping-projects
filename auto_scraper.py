import requests
from bs4 import BeautifulSoup as bsp
import csv
import time
import random




class Pro:
    def __init__ (self, link, tag_list, scrape_items, file_name, file_mode):

        self.fieldnames = scrape_items
        self.link = link
        detail = []

        response = link_opner(self.link)

        if response is not None :

            soup = bsp(response.text, 'html.parser')

            for list_ in tag_list :

                tag_cl = " ".join(list_)
                a = soup.select_one(tag_cl)
                if a:
                    a = a.get_text(strip=True)
                else:
                    a = 'N/A'

                detail.append(a)


            csv_file = dict(zip(scrape_items, detail))


            if file_mode == 'w':
                with open(file_name, 'w', newline='', encoding='utf-8') as file:
                    writer = csv.DictWriter(file, fieldnames = self.fieldnames)
                    writer.writeheader()

                    writer.writerow(csv_file)


            elif file_mode == 'a':
                with open(file_name, 'a', newline='', encoding='utf-8') as file:
                    writer = csv.DictWriter(file, fieldnames = self.fieldnames)
                    writer.writerow(csv_file)


def link_opner(url):

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0"
            }

        response = requests.get(url, headers = headers , timeout = 10)
        response.raise_for_status()
        response.encoding ="utf-8"
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
    except requests.exceptions.MissingSchema:
        print("There is not website url ", url)

while True:
    url = input("Enter Url :")
    response = link_opner(url)
    if not response :
        continue
    else :
        break

while True:
    print("How much things You want to scrape write them to sperate by ','")
    want = input("How much things You want : ").strip()
    if want :
        scrape_items = want.split(",")
        break
    else :
        continue


text_tags = [
    # Headings
    'h1', 'h2', 'h3', 'h4', 'h5', 'h6',

    # Common Text Blocks
    'p', 'span', 'div', 'section', 'article', 'aside',

    # Inline Formatting
    'b', 'strong', 'i', 'em', 'u', 'mark', 'small', 'del', 'ins', 'sub', 'sup',

    # Links and Buttons
    'a', 'button', 'label',

    # Lists
    'li', 'dt', 'dd',

    # Advanced/Semantic Text
    'blockquote', 'q', 'cite', 'pre', 'code', 'kbd', 'samp', 'time', 'address'
]

link_tags_list = ['a', 'area', 'link']


print("Do you want to extract tags from other pages in your web scraping?")
p = input("|Yes or No|: ").strip().lower()
if p in ['yes', 'ha', 'yea', 'y']:
    while True :
        page_links = input("Write your link tag sturcture : ")
        if page_links != '':
            page_links = page_links.split()
            last_tag = page_links[-1].split('.')[0]
            if all(item_tag.split('.')[0] in text_tags for item_tag in page_links) and last_tag in link_tags_list:
                break
            else :
                continue
else :
    page_links = None



tag_list = []
for tg in scrape_items :

    while True :
        tag = input(f"what tag for {tg} :").strip()

        if tag != '':
            tag = tag.split()
            last_tag = tag[-1]
            if all(tag_.split('.')[0] in text_tags for tag_ in tag):
                if '.' not in last_tag:
                    c = input(f"for {last_tag} tag's class or not : ").strip()
                    if c not in ['', 'no', 'not', 'n']:
                        if '.' in cl:
                            tag[-1] = tag[-1]+cl
                            tag_list.append(tag)
                            break
                        else :
                            tag[-1] = f'{tag[-1]}.{cl}'
                            tag_list.append(tag)
                            break
                    else :
                        tag_list.append(tag)
                        break
                else :
                    tag_list.append(tag)
                    break
            else :
                continue
        else:
            continue


while True :
    file_name = input("Enter Your File Name : ")
    if file_name:
        if '.csv' not in file_name:
            file_name = f'{file_name}.csv'
        try :
            with open(file_name, 'r') as f :
                reader = csv.reader(f)
                print("This File is exist")
                user = input("Do you want to overwrite file or add new data :").strip().lower()
                if user in ['append', 'add', 'new']:
                    existing_header = next(reader)
                    if existing_header == scrape_items:
                        file_mode = "a"
                        break
                    else :
                        print("Header is not match bro pls try again")
                        continue

                elif user in ['overwrite', 'write']:
                    file_mode = 'w'
                    break
                else :
                    print("rename bro ")
                    continue
        except FileNotFoundError:
            file_mode = 'w'
            break
    else :
        continue

print(tag_list)

base_url = url

if page_links is not None:
    page_links = " ".join(page_links)
    response = link_opner(url)
    soup = bsp(response.text, 'html.parser')
    all_links = soup.select(page_links)
    for link in all_links :
        link = link.get('href')
        print(link)
        if 'https://'+url not in link:
            url = f'{url}/{link}'
            print(url)
        else :
            url = link
        b = Pro(url, tag_list, scrape_items, file_name, file_mode)
        url = base_url
        file_mode = 'a'


b = Pro(url, tag_list, scrape_items, file_name, file_mode)
