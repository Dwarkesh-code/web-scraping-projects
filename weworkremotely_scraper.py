import requests
from bs4 import BeautifulSoup as bsp
import pandas as pd
import time
import random

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


def remote_job_page_opner(url):


    response = link_opner(url)
    soup = bsp(response.text, 'html.parser')


    title = soup.select_one('h1.lis-container__header__hero__company-info__title')
    if title:
        title = title.get_text(strip = True)
    else :
        title = 'N/A'

    container = soup.select_one('div.lis-container__job__sidebar')
    if container:
        company_name = container.select_one('div.lis-container__job__sidebar__companyDetails__info__title h3')
        if company_name:
            company_name = company_name.get_text(strip=True)
        else :
            company_name = 'N/A'
        location = container.select_one('li.lis-container__job__sidebar__job-about__list__item:-soup-contains("Region") span.box--region')
        if location:
            location = location.get_text(strip=True)
        else:
            location = 'Not Anywhere in the World'
        salary = soup.select_one('li.lis-container__job__sidebar__job-about__list__item:-soup-contains(" Salary ") a span.box--blue')
        if salary:
            salary = salary.get_text(strip=True)
        else:
            salary = 'Not Mentioned'
        job_type = container.select_one('li.lis-container__job__sidebar__job-about__list__item:-soup-contains(" Job type ") a span.box--jobType')
        if job_type:
            job_type = job_type.get_text(strip=True)
        else:
            job_type = 'Not Mentioned'
        catagory = container.select_one('li.lis-container__job__sidebar__job-about__list__item:-soup-contains(" Category ") a span.box--blue')
        if catagory:
            catagory = catagory.get_text(strip=True)
        else:
            catagory = 'N/A'
        last_date = container.select_one('li.lis-container__job__sidebar__job-about__list__item:-soup-contains(" Apply before ") span')
        if last_date:
            last_date = last_date.get_text(strip=True)
        else:
            last_date='N/A'

        return title, company_name, location, salary, job_type, catagory, last_date


def csv_saver(detail_df):
    try:
        old_file = pd.read_csv('Remoteok.csv')

        combined_file = pd.concat([old_file, detail_df]).drop_duplicates(subset=['Page Link'], keep='first')

        combined_file.to_csv('Remoteok.csv', index=False, encoding='utf-8-sig')

    except FileNotFoundError:
        detail_df.to_csv('Remoteok.csv', index =False, encoding='utf-8-sig')



url = 'https://weworkremotely.com/'

response = link_opner(url)
soup = bsp(response.text, 'html.parser')

page_links=  soup.select('li.new-listing-container.feature a.listing-link--unlocked')



detail = {
    'Title':[],
    'Company Name':[],
    'Location':[],
    'Salary':[],
    'Job Type':[],
    'Catagory':[],
    'Last Date To Apply':[],
    'Page Link':[]
    }
n=0
for page_link in page_links:
    if page_link:
        page_link = page_link['href']
        if 'https://weworkremotely.com' not in page_link:
            page_link= f'https://weworkremotely.com{page_link}'

        num = random.uniform(1,4)
        time.sleep(num)


        title, company_name, location, salary, job_type, catagory, last_date = remote_job_page_opner(page_link)
        n +=1
        print(n)


        detail['Title'].append(title)
        detail['Company Name'].append(company_name)
        detail['Location'].append(location)
        detail['Salary'].append(salary)
        detail['Job Type'].append(job_type)
        detail['Catagory'].append(catagory)
        detail['Last Date To Apply'].append(last_date)
        detail['Page Link'].append(page_link)

    detail_df = pd.DataFrame(detail)

    csv_saver(detail_df)
