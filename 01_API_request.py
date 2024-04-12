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
