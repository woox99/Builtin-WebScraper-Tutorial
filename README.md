# API Web Scraping Tutorial
### Introduction

This tutorials covers step by step instructions for scraping companies and their technologies off the job posting board builtin.com.

* This tutorial uses ``API requests`` to retrieve responses containing the data we want to scrape.

* Understanding the basics of the ``Python`` language and the basics of making API calls with an API platform such as ``Postman`` is the only prerequisites for this tutorial.

## Step 0.1: Investigating the Site for the API
Lets start investigating the site: https://builtin.com

 On each company's page of the site, there is a list of technologies that the company uses and the technology category. This is the data that we are interested in scraping.

Instead of making a script to scrape each company page of the site (over 50,000+ pages), lets investigate whether there is an API that we can access by making a request to it.

If we use the ``inspect tool`` on a companies page and navigate to ``Network`` -> ``Fetch/XHR`` we can see a list of requests that our client is making when the page loads. Multiple of these are APIs.

* If we check the ``Response`` of each one, we find that one of them send back a json response with the structure of:
```javascript
{
    "data": {
        "companyByID": {
            "technologies": [
                {
                    "name": "XYZ",
                    "urlName": "XYZ",
                    "categoryName": "XYZ/XYZ"
                },
            ],
        }
    }
}
```

* If we check the ``Header`` sent with the request we can see that this is a ``POST method`` request.

* If we check the ``Payload`` of this request, it has the structure:
```javascript
{
        "operationName": "GetCompanyTechnologies",
        "query": "XYZ",
        "variables": {
        "id": 12345
    }
}
```

It looks we have found an API that given a company's unique id, it responds with a json of its technologies. Perfect. Navigate to any company's page and copy the payload object.

Open Postman or a similar API platform, and make a request to the ``API domain`` and copy the payload in a ``raw`` ``json`` ``body`` of the request and set the request to POST.

If you've done everything correctly, it will return with a json object of the companies technologies. 

## Step 0.2: Investigating the Site for company's IDs

Now we need a way to collect all off the companies' IDs so we can make a script that makes the API request for each ID.


Inspecting the HTML on the list of companies page: https://builtin.com/companies we find that each company element has a child-element with the attribute:
```html
my-i<my-item entity-id='12345'></my-item>
```

This is how we will collect the companies' IDs.

## Step 0.3: Deciding How to Structure our Data 

From the data we are able to collect, the data will be structured as such:
| Company ID | Company Name | Tech Name | Tech Category |
|-----------------|-----------------|-----------------|-----------------|
| 12345    | Facebook   | JavaScript    | Language    |
| 12345    | Facebook   | React    | Library    |

### The roadmap of our scraper will look something like this:
* For each company on the list of companies page https://builtin.com/companies -> collect Company ID and Company Name
* For each Company ID collected -> make the API request to retrieve a list of it's technologies
* For each technology collected -> append a new data entry to a .csv file with the above structure
* Repeat for each page of list of companies (handle pagination)



## Step 1.0: Create and Setup Project Folder
Let's get started on building our scraper.

* Create a new project folder
* Create a virtual environment to isolate your dependencies. In your terminal, within the project folder enter the command:
```
python -m venv venv
```
* Activate the virtual environment with the command:
```
python -m venv venv
```
* Install the necessary dependencies for this project with the follow command(s):
```
pip3 install httpx selectolax requests
```

* You should now have a directory named ``venv`` within your project folder. 
* Optional: copy the ``.gitignore`` file if you're pushing to Github.

## Step 2.0: Create API Request Script
Create a new file named ``api_request.py`` on the same level as the virtual environment (not inside the environment).

In this file let's start creating the script that will make the API call with the appropriate ``Headers`` and ``Payload``:

**(This file will correspond to the file ``01_API_request.py`` in this repository)**

```python
import requests
import json

url = "https://api.builtin.com/graphql"

payload = json.dumps({
        "operationName": "GetCompanyTechnologies",
        "query": "query GetCompanyTechnologies($id: Int!) {\n  companyByID(id: $id) {\n    technologies {\n      name\n      urlName\n      categoryName\n    }\n    extraTechnologies {\n      name\n      categoryName\n    }\n  }\n}\n",
        "variables": {
        "id": 53986
    },
})
headers = {
    'Content-Type': 'application/json',
    'Cookie': '__cf_bm=CAwtfM0WyHGGmHy5u92fExtmJGCHhKGJ5Lvo7gOBCVU-1712722592-1.0.1.1-P6GE6pWWS6kb3WQEAwSJuAcOcP5H1T4th56_J1AjUS0rOj65dUOY6yght_u.p5Iub1BAWC89I74fooNshuP25A'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.json())
```

* In this code, we are manually setting the ``"id": 53986`` which is the ID of the company 'Afterpay'.
* ``requests.request()`` makes a request with the ``POST method``, to the ``url``, attaching the ``headers`` and ``payload``
* We set ``response =`` to the API reponse object.


When we run this code, our console prints reponse object that will look like this:
```
{'data': {'companyByID': {'technologies': [{'name': 'Java', 'urlName': 'java', 'categoryName': 'engineering/languages'}, {'name': 'JavaScript', 'urlName': 'javascript', 'categoryName': 'engineering/languages'}, {'name': 'Kotlin', 'urlName': 'kotlin', 'categoryName': 'engineering/languages'}, {'name': 'MySQL', 'urlName': 'mysql', 'categoryName': 'engineering/databases'}, {'name': 'Node.js', 'urlName': 'node-js', 'categoryName': 'engineering/frameworks'}, {'name': 'React', 'urlName': 'react', 'categoryName': 'engineering/libraries'}, {'name': 'Spring', 'urlName': 'spring', 'categoryName': 'engineering/frameworks'}, {'name': 'Teradata', 'urlName': 'teradata', 'categoryName': 'engineering/databases'}], 'extraTechnologies': [{'name': 'css', 'categoryName': 'engineering/languages'}, {'name': 'html', 'categoryName': 'engineering/languages'}, {'name': 'kafka', 'categoryName': 'engineering/languages'}]}}}
```

We only want the ``technologies``, not the `extraTechnologies`, and we only want the technologies that fall under the ``engineering/`` category so can clean this up a bit by adding the follow lines of code to our ``api_request.py`` script:

```python
# ..previous code here

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
```

Now when we run our code, we get a nice clean list of dictionaries containing each technology this company uses:

```
{'name': 'Java', 'category': 'engineering/languages'}
{'name': 'JavaScript', 'category': 'engineering/languages'}
{'name': 'Kotlin', 'category': 'engineering/languages'}    
{'name': 'MySQL', 'category': 'engineering/databases'}     
{'name': 'Node.js', 'category': 'engineering/frameworks'}  
{'name': 'React', 'category': 'engineering/libraries'}     
{'name': 'Spring', 'category': 'engineering/frameworks'}   
{'name': 'Teradata', 'category': 'engineering/databases'}
```

This is how we will handle the API call for each ID but we need another script that handles the collection of the Company IDs.

## Step 2.0: Create httpx Get Script
Create a new file named ``get_company_id.py`` on the same level as the previous.

In this file let's start creating the script that will use ``httpx`` to make a ``GET request`` to get the site's ``HTML`` so we can scrape the company's IDs from the element:
```html
<my-item entity-id='12345'></my-item>
```

**(This file will correspond to the file ``02_get_company_id.py`` in this repository)**

You need to set ``'User-Agent' :`` to your actual user agent. To do this simply google 'What is my user agent?' and copy your user agent from the browser.

```python
import httpx
from selectolax.parser import HTMLParser

url = 'https://builtin.com/companies'

headers = {
    'User-Agent' : 'copy_your_user_agent_here'
}

res = httpx.get(url, headers=headers, follow_redirects=True)

print(f'Status Code: {res.status_code}') # Console annotation
print(res)
```

In this code we are making a ``GET request`` similarly to what your browser does, to get the http response of the site https://builtin.com/companies, where the companies are listed.

When we run the code (make sure your venv is activated), our cosole prints the status of the request, along with the response object:

```
Status Code: 200
<Response [200 OK]>
```

If you're getting a status code other than ``Status Code: 200`` it could mean a number of different things. Heres the documentation for httpx reguarding difference status codes:

https://www.python-httpx.org/quickstart/#response-status-codes

We need to turn the reponse object into something more flexible that we can extract data from. Add these lines of code to the script:

```python
# previous code here..

html = HTMLParser(res.text)

companies = html.css('div.company-unbounded-responsive')

for company in companies:
    print(company.css_first('my-item').attributes.get('entity-id'))
```

Let's walk through this code step by step:

* ``HTMLParser()`` parses the response into html
* ``html.css()`` captures all ``div`` elements on the page with the the ``class="company-unbounded-responsive"``
* For each div element in ``companies`` we want to get the first ``my-item`` element, and get it's attribute ``entity-id`` which stores the company's ID

When we run our code our console will print the ID for every company element on the page:
```
63791
63811
63899
63930
63978
64027
64058
64116
Traceback (most recent call last):
  File "C:\Users\janul\OneDrive\Desktop\BuiltinWebScraper\02_get_company_id.py", line 20, in <module>   
    print(company.css_first('my-item').attributes.get('entity-id'))
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AttributeError: 'NoneType' object has no attribute 'attributes'
```

We get this ``AttributeError`` because it appears that there are some hidden company elements that don't show up on the page and don't have the ``entity-id`` attribute associated with them.

Let's include error handling to ignore any company elements that don't have and ID:

```python
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
    # Here we could implement the api_request.py script
```

Here we could implement the ``api_request.py`` script to request the technologies object for each company ID but this will only scrape the technologies for each company on the first page. We want our script to automatically scrape each page containing the companies (handle pagination).

## Step 2.1: Creating Functions & Handling Pagination

**(This code corresponds to the file ``03_pagination.py`` in this repository)**

Let's clean up our code by creating some functions:

```python
import httpx
from selectolax.parser import HTMLParser

def get_html(url, page):
    pass
    
def parse_search_page(html):
    pass

def id_exists(company):
    try:
        return company.css_first('my-item').attributes.get('entity-id')
    except AttributeError:
        return False

def main():
    pass

if __name__ == '__main__':
    main()
```

* ``main():`` will handle the pagination:
```python
def main():
    url = 'https://builtin.com/companies?page='

    for page in range(1,3):

        print(f'Scraping Page: {page}') # Console annotation

        html = get_html(url, page)
        companies = parse_search_page(html)

        for company in companies:
            print(company)
            # This is where we are going to fetch the technologies for each company later..
```

* ``get_html(url, page):`` will take the url and page and return the html for that page. If the exception doesn't get a reponse from the page, we will return ``False`` and skip the page:
```python
def get_html(url, page):

    headers = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
    }

    res = httpx.get(url + str(page), headers=headers, follow_redirects=True)

    print(f'Status Code: {res.status_code}') # Console annotation

    try:
        res.raise_for_status()
    except httpx.HTTPStatusError as exc:
        print(f"Error response {exc.response.status_code} while requesting {exc.request.url!r}.")
        return False

    html = HTMLParser(res.text)
    return html
```

* ``parse_search_page(html):`` will take in the html from each page and yield out a dictionary containing the ``{Company ID, Company Name}`` for each company on that page:

```python
def parse_search_page(html):
    companies = html.css('div.company-unbounded-responsive')

    for company in companies:
        if id_exists(company):
            data = {
                'id': (company.css_first('my-item').attributes.get('entity-id')),
                'name': company.css_first('h2.company-title-clamp').text()
            }
            yield data
```

Now our script does the same thing as ``get_company_id.py`` but for each page on the site. Now we need to make a function that contains the ``api_request.py`` script so we can fetch the technologies for each company and combine it into our dictionaries that we will later export into a .csv file.

## Step 3.0: Combining Scripts

**(This code corresponds to the file ``04_get_technologies.py`` in this repository)**

We will create a ``dataclass`` to store the entries in instead of using dictionaries so lets import that, and lets import csv since we will use it later:

```python
from dataclasses import dataclass, asdict, fields
import csv
import json

@dataclass
class Tech:
    entity_id: str
    company_name: str
    tech_name: str
    tech_category: str

# previous code here..
```

Let's create a function ``get_company_techs(entity_id, company_name):`` that will essentially be the functionality of our earlier created ``api_request.py`` script, but we will change it slightly to encompase the Company ID, and Company Name in the dataclass:

```python
def get_company_techs(entity_id, company_name):
    try:
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

        for tech in techs:
            if 'engineering' in tech['categoryName']:
                new_tech = Tech(
                    entity_id = str(entity_id),
                    company_name = company_name,
                    tech_name = tech['name'],
                    tech_category = tech['categoryName']
                )
                append_to_csv(asdict(new_tech))
    except Exception as e:
        print(f"An error occured while processing {company_name}: {str(e)}")
```
We also need to change our main function:

```python
def main():
    url = 'https://builtin.com/companies?page='
    for page in range(1,3):
        print(f'Getting html for page: {page}') # Console annotation
        html = get_html(url, page)
        companies = parse_search_page(html)

        for company in companies:
            get_company_techs(company['id'], company['name'])
```

Notice that in the ``get_company_techs()`` function, there is another function ``append_to_csv()`` that we haven't created yet, which leads us to our last step..

## Step 4.0: Creating .csv File

**(This code corresponds to the file ``05_appending_to_csv.py`` in this repository)**

Lets create a function ``append_to_csv(asdict(tech))`` that will take in a tech and save it to a .csv file:

```python
def append_to_csv(tech):
    field_names = [field.name for field in fields(Tech)]
    with open('append.csv', 'a', newline='') as f:
        writer = csv.DictWriter(f, field_names)
        writer.writerow(tech)
```

Now for every technology that is scraped off the site, we will append the dataclass to a .csv file named append.csv with our data stuctured like this:
| Company ID | Company Name | Tech Name | Tech Category |
|-----------------|-----------------|-----------------|-----------------|
| 12345    | Facebook   | JavaScript    | Language    |
| 12345    | Facebook   | React    | Library    |

Finally, I created the ``append.xlsx`` file that has the cleaned up category collumn and created a dashboard out of the data collected. Ultimately, after scraping over 50,000 companies, there was only technologies listed for approximately 2200 of them.

### API Request Tutorial Video 
https://www.youtube.com/watch?v=DqtlR0y0suo&t=184s


