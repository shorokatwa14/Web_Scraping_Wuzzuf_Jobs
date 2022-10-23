# 1st step install and import modules
    #-- pip/pip3 install lxml
    #-- pip/pip3 install requests
    #-- pip/pip3 install beautifulsoup4
import requests
from bs4 import BeautifulSoup
import csv
from itertools import zip_longest
import pandas as pd
import chardet

page = 0
# Creating lists to save data
job_title = []
company_name = []
location = []
skills = []
links = []
salary = []
requirement = []
date = []

while True:
    # use requests to fetch the url
    try:
        result = requests.get(f"https://wuzzuf.net/search/jobs/?a=hpb%7Cspbl&q=python&start={page}")
        src = result.content
        soup = BeautifulSoup(src,"html.parser")

        page_limit = int(soup.find('strong').text)

        if page > (page_limit // 15):
            print('DONE: Pages ended, terminate...')
            break
        #find the elements we need
        job_titles = soup.find_all('h2', {'class': 'css-m604qf'})
        company_names = soup.find_all('a', {'class': 'css-17s97q8'})
        locations = soup.find_all('span', {'class': 'css-5wys0k'})
        job_skills = soup.find_all('div', {'class': 'css-y4udm8'})
        posted_new = soup.find_all('div', {'class': 'css-4c4ojb'})
        posted_old = soup.find_all('div', {'class': 'css-do6t5g'})
        posted = [*posted_new, *posted_old]

        # loop over returned lists to extract needed info into othe lists
        for i in range(len(job_titles)):
            job_title.append(job_titles[i].text)
            links.append(job_titles[i].a.attrs['href'])
            company_name.append(company_names[i].text)
            location.append(locations[i].text)
            skills.append(job_skills[i].text)
            date.append(posted[i].text)

        page += 1
        print('SUCCESS: Page switched...')
    except:
         print("FAILEID: Error occured...")
         break

#create csv file and fill it with values
def save_to_csv():
    file_list = [job_title, company_name, date, location, skills, links]
    exported = zip(*file_list)
    with open('C:\\Users\\COMPUMARTS\\Downloads\\jobs_scrapping.csv',"w") as file:
        wr = csv.writer(file)
        wr.writerow(["job title", "company name","Date", "location", "skills",'links'])
        wr.writerows(exported)
    print(" DONE!")
save_to_csv()
