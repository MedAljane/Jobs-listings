import bs4
from bs4 import BeautifulSoup
import requests
import pandas as pd

jobsList = ["Shop Manager",
"Artificial Intelligence Engineer",
"Restaurant Specialist",
"Marketer",
"Dietary Aide",
"Development Team Lead",
"Beauty Advisor",
"Nursing Manager",
"Receptionist",
"SAP ABAP Developer",
"Head of Revenue Operations",
"Human Resources Analytics Manager",
"Diversity and Inclusion Manager",
"Truck Driver",
"Employee Experience Manager",
"Sales Enablement Specialist",
"Advanced Practice Provider",
"Growth Marketing Manager",
"Data Governance Manager",
"Grants Management Specialist",
"Molecular Technologist",
"Content Designer",
"Sustainability Analyst",
"Strategy & Operations Manager",
"Chief People Officer",
"Sales Development Representative",
"Online Campaign Manager",
"Product Operations Manager",
"Sales Compensation Manager",
"Customer Marketing Manager",
"Head of Rewards",
"Deal Manager",
"Customer Success Associate",
"Channel Account Executive",
"Director of Bioinformatics"
]

# Create an empty DataFrame with columns
data = {
    'Link': [],
    'Job title': [],
    'Company name': [],
    'Location': [],
    'Salary min':[],
    'Salary max':[],
    'Description': [],
    'Seniority level': [],
    'Employment type': [],
    'Job function': [],
    'Industries': []
}

for job in jobsList[:5]:
    for num in range(25, 50, 25):
        print(f"request for {num}")
        response = requests.get(f'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/{job}-jobs?position=1&pageNum=0&start={num}')
        soup = BeautifulSoup(response.text, 'html.parser')
        length_results = len(soup.find_all('li'))
        for number, li in enumerate(soup.find_all('li')):
            print(f"result {number}/{length_results}")
            try:
                salary = li.find('span', class_='job-search-card__salary-info').text.strip()
            except:
                salary = 'not Found'
            try:
                link = li.find('a', class_='base-card__full-link').get('href')
            except:
                continue
            print(link)

            soup2 = BeautifulSoup(requests.get(link).text, 'html.parser')
            crits = {}
            try:
                for li in soup2.find('ul', class_='description__job-criteria-list').find_all('li'):
                    crits[li.find('h3').text.strip()] = li.find('span').text.strip()
            except:
                pass

            data['Link'].append(link)

            try:
                if '-' in salary:
                    sal_min, sal_max = tuple(salary.split('-'))
                    print(f"min sal:{sal_min}, max sal:{sal_max}")
                    data['Salary min'].append(sal_min.trim().strip())
                    data['Salary max'].append(sal_min.trim().strip())
                else:
                    data['Salary min'].append(salary)
                    data['Salary max'].append(salary)

            except:
                data['Salary min'].append('not Found')
                data['Salary max'].append('not Found')

            try:
                data['Job title'].append(soup2.find('h1', class_='topcard__title').text.strip())
            except:
                data['Job title'].append('not Found')

            try:
                data['Company name'].append(soup2.find('a', class_='topcard__org-name-link topcard__flavor--black-link').text.strip())
            except:
                data['Company name'].append('not Found')

            try:
                data['Location'].append(soup2.find('span', class_='topcard__flavor topcard__flavor--bullet').text.strip())
            except:
                data['Location'].append('not Found')
                
            try:
                data['Description'].append(soup2.find('div', class_='show-more-less-html__markup').text.strip())
            except:
                data['Description'].append('not Found')
                

            data['Seniority level'].append(crits['Seniority level'] if 'Seniority level' in crits.keys() else None)
            data['Employment type'].append(crits['Employment type'] if 'Employment type' in crits.keys() else None)
            data['Job function'].append(crits['Job function'] if 'Job function' in crits.keys() else None)
            data['Industries'].append(crits['Industries'] if 'Industries' in crits.keys() else None)

df = pd.DataFrame(data)

from datetime import datetime
fName = f'Jobs_{datetime.now().strftime("%m-%d-%Y_%Hh%M")}.csv'
df.to_csv(fName, index=False)