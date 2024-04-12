import httpx
from selectolax.parser import HTMLParser
import time
import requests
import json
from dataclasses import dataclass, asdict, fields
import csv

@dataclass
class Tech:
    entity_id: str
    company_name: str
    tech_name: str
    tech_category: str

def get_html(url, page):

    headers = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
    }

    res = httpx.get(url + str(page), headers=headers, follow_redirects=True)

    print(f'Status Code: {res.status_code}') # Console annotation

    html = HTMLParser(res.text)
    return html

def id_exists(company):
    try:
        return company.css_first('my-item').attributes.get('entity-id')
    except AttributeError:
        return False
    
def parse_search_page(html):
    companies = html.css('div.company-unbounded-responsive')

    for company in companies:
        if id_exists(company):
            data = {
                'id': int(company.css_first('my-item').attributes.get('entity-id')),
                'name': company.css_first('h2.company-title-clamp').text()
            }
            yield data

def get_company_techs(entity_id, company_name):
    url = "https://api.builtin.com/graphql"

    payload = json.dumps({
            "operationName": "GetCompanyTechnologies",
            "query": "query GetCompanyTechnologies($id: Int!) {\n companyByID(id: $id) {\n technologies {\n name\n urlName\n categoryName\n }\n extraTechnologies {\n name\n categoryName\n }\n }\n}\n",
            "variables": {
            "id": entity_id
            }
        })
    headers = {
        'Content-Type': 'application/json',
        'Cookie': '__cf_bm=CAwtfM0WyHGGmHy5u92fExtmJGCHhKGJ5Lvo7gOBCVU-1712722592-1.0.1.1-P6GE6pWWS6kb3WQEAwSJuAcOcP5H1T4th56_J1AjUS0rOj65dUOY6yght_u.p5Iub1BAWC89I74fooNshuP25A'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    data = response.json()
    techs = data['data']['companyByID']['technologies']

    tech_list = []

    for tech in techs:
        new_tech = {
            'name':tech['name'],
            'category':tech['categoryName']
        }
        if 'engineering' in new_tech['category']:
            tech_list.append(new_tech)

    for tech in tech_list:
        print(tech)


def main():
    url = 'https://builtin.com/companies?page='
    for page in range(1,3):
        print(f'Getting html for page: {page}') # Console annotation
        time.sleep(2)
        html = get_html(url, page)
        companies = parse_search_page(html)

        for company in companies:
            get_company_techs(company['id'], company['name'])

if __name__ == '__main__':
    main()