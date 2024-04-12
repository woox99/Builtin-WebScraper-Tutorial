import httpx
from selectolax.parser import HTMLParser

url = 'https://builtin.com/companies'

headers = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
}

res = httpx.get(url, headers=headers, follow_redirects=True)

print(f'Status Code: {res.status_code}') # Console annotation
# print(res)

html = HTMLParser(res.text)

companies = html.css('div.company-unbounded-responsive')

entity_ids = []

def id_exists(company):
    try:
        return company.css_first('my-item').attributes.get('entity-id')
    except AttributeError:
        return False
    
for company in companies:
    if id_exists(company):
        entity_ids.append(company.css_first('my-item').attributes.get('entity-id'))

for id in entity_ids:
    print(id)