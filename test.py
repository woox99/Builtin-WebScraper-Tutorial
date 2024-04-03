import httpx
from selectolax.parser import HTMLParser
import time

def get_html(url):
    headers = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
    }
    res = httpx.get(url, headers=headers, follow_redirects=True)
    print(res.text)
    print(f'Status code: {res.status_code}') # Console annotation

    try:
        res.raise_for_status()
    except httpx.HTTPStatusError as exc:
        print(f"Error response {exc.response.status_code} while requesting {exc.request.url!r}.")
        return False
    html = HTMLParser(res.text)
    return html


def main():
    url = 'https://builtin.com/job/infrastructure-engineer-ii-restaurant-systems-management/2411243'

    html = get_html(url)




if __name__ == '__main__':
    main()