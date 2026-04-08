import csv
import requests
from bs4 import BeautifulSoup as bsp


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0"
    }

url = "https://realpython.github.io/fake-jobs/"

with open ("job_csv.csv", "w", newline = "", encoding = "utf-8") as file :
    fieldnames = ['Job Title', 'Company', 'Location', 'Time']
    writer = csv.DictWriter(file, fieldnames = fieldnames)
    writer.writeheader()
    n = 0
    try :
        response = requests.get(url, headers = headers , timeout = 10)
        response.raise_for_status()
        soup = bsp(response.text, 'html.parser')

        jobs = soup.select("div.container div.column.is-half div.card-content")

        for job in jobs:
            job_t = job.select_one("div.media-content h2.title.is-5")
            job_title = job_t.text if job_t else "N/A"
            job_c = job.select_one("div.media-content h3.subtitle.is-6.company")
            job_company = job_c.text if job_c else "N/A"
            loc = job.select_one("div.content p.location ")
            location = loc.text if loc else "N/A"
            date_tag = job.select_one("div.content p.is-small.has-text-grey time")
            date_time = date_tag.get("datetime") if date_tag else "N/A"
            location = location.strip()
            n +=1
            print(f"{n}. Job : {job_title}")
            print(f"Company : {job_company}")
            print("Location : ",location )
            print("Date and Time : ",date_time)
            csv_file = {'Job Title': job_title, 'Company': job_company, 'Location': location, 'Time': date_time}
            writer.writerow(csv_file)



    except requests.exceptions.Timeout:
        print("Time Out")
        print("Can't reach the site ")

    except requests.exceptions.ConnectionError:
        print("Internet is off")

    except requests.exceptions.HTTPError as e :
        print(f"Error : {e}")

