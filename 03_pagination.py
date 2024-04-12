import httpx
from selectolax.parser import HTMLParser
import time

def get_html(url, page):

    headers = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
    }

    res = httpx.get(url + str(page), headers=headers, follow_redirects=True)

    time.sleep(1)
    print(f'Status Code: {res.status_code}') # Console annotation

    try:
        res.raise_for_status()
    except httpx.HTTPStatusError as exc:
        print(f"Error response {exc.response.status_code} while requesting {exc.request.url!r}.")
        return False
    html = HTMLParser(res.text)
    return html

    
def parse_search_page(html):
    companies = html.css('div.company-unbounded-responsive')

    for company in companies:
        if id_exists(company):
            data = {
                'id': (company.css_first('my-item').attributes.get('entity-id')),
                'name': company.css_first('h2.company-title-clamp').text()
            }
            yield data

def id_exists(company):
    try:
        return company.css_first('my-item').attributes.get('entity-id')
    except AttributeError:
        return False

def main():
    url = 'https://builtin.com/companies?page='

    for page in range(1,3):

        print(f'Scraping Page: {page}') # Console annotation
        time.sleep(2)

        html = get_html(url, page)
        companies = parse_search_page(html)

        for company in companies:
            print(company)

if __name__ == '__main__':
    main()