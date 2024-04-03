import httpx
from selectolax.parser import HTMLParser
import time
# from urllib.parse import urljoin
from dataclasses import dataclass, asdict

@dataclass
class Company:
    entity_id : str
    company_name : str
    tech_name : str
    tech_type : str

def get_html(url, **kwargs):
    headers = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
    }

    if kwargs.get('page'):
        res = httpx.get(url + str(kwargs.get('page')), headers=headers, follow_redirects=True)
    else:
        res = httpx.get(url, headers=headers, follow_redirects=True)

    print(f'Status code: {res.status_code}') # Console annotation

    try:
        res.raise_for_status()
    except httpx.HTTPStatusError as exc:
        print(f"Error response {exc.response.status_code} while requesting {exc.request.url!r}.")
        return False
    html = HTMLParser(res.text)
    return html

# Some company elements on page are emtpy so this function checks if there is an id associated with the company element
def id_exists(company):
    try:
        return company.css_first('my-item').attributes.get('entity-id')
    except AttributeError:
        return False
    
def parsed_company_page(html):
    print(html)
    # print(html.css_first('div.header-title'))
    # new_company = Company(
    #     entity_id = html.css_first('div.header-title h2').text()
    # )
    # print(new_company)
    # companies = html.css('div.company-unbounded-responsive')

    # for company in companies:
    #     if id_exists(company):
    #         item = {
    #             'Entity-ID' : company.css_first('my-item').attributes.get('entity-id'),
    #             'Company Name' : company.css_first('h2.company-title-clamp').text()
    #         }
    #         yield item

def parsed_search_page(html: HTMLParser):
    companies = html.css('div.company-unbounded-responsive')
    for company in companies:
        if id_exists(company):
            yield company.css_first('a').attributes['href']

def main():
    url = 'https://builtin.com/companies?page='
    companies = []

    for page in range(1, 2):
        html = get_html(url, page=page)
        if html is False:
            break

        company_urls = parsed_search_page(html)

        for company_url in company_urls:
            print(company_url)
            print(f"Scraping page: {company_url}") # Console Annotation
            html = get_html(company_url)
            companies.append(parsed_company_page(html))
            time.sleep(5)

        for company in companies:
            print(asdict(company))

if __name__ == '__main__':
    main()