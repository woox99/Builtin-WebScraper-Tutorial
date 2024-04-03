import httpx
from selectolax.parser import HTMLParser
import time

# This scrapes companies and their id's on the company search page
# request.py will scrape techs from the api request using company ids
def get_html(url, page):
    headers = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
    }
    res = httpx.get(url + str(page), headers=headers, follow_redirects=True)

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
    
def parse_search_page(html):
    companies = html.css('div.company-unbounded-responsive')

    for company in companies:
        if id_exists(company):
            item = {
                'Entity-ID' : company.css_first('my-item').attributes.get('entity-id'),
                'Company Name' : company.css_first('h2.company-title-clamp').text()
            }
            yield item

def main():
    url = 'https://builtin.com/companies?page='
    for page in range(1, 2):
        print(f"Scraping page: {page}") # Console Annotation
        html = get_html(url, page)
        if not html:
            break
        data = parse_search_page(html)
        time.sleep(5)
    for item in data:
        print(item)

if __name__ == '__main__':
    main()