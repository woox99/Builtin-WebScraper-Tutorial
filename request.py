import requests
import json
from dataclasses import dataclass, asdict

@dataclass
class Tech:
    entity_id: str
    company_name: str
    tech_name: str
    tech_category: str

url = "https://api.builtin.com/graphql"

payload = json.dumps({
    "operationName": "GetCompanyTechnologies",
    "query": "query GetCompanyTechnologies($id: Int!) {\n companyByID(id: $id) {\n technologies {\n name\n urlName\n categoryName\n }\n extraTechnologies {\n name\n categoryName\n }\n }\n}\n",
    "variables": {
    "id": 63899
    }
})
headers = {
    'Content-Type': 'application/json',
    'Cookie': '__cf_bm=ZeNfR0EkBcvQlfEIOy1RSpX2Qn62TDVjeo56SI7G_WY-1712182970-1.0.1.1-03XZzLV25fTbcZhcoV.tAX3VeSiWsYYDPL3WjxLqDzJrMh6VdjAe7cwOjVXZE5ZDLmxODnP4c8_BBbD74YTT6A'
}

res = requests.request("POST", url, headers=headers, data=payload)

# watch the rest of the video to find out how to use pandas to easily convert json to csv
data = res.json()
# add data['extraTechnologies']
techs = data['data']['companyByID']['technologies']

tech_list = []

for tech in techs:
    if 'engineering' in tech['categoryName']:
        new_tech = Tech(
            entity_id =63899,
            company_name = 'grinder',
            tech_name = tech['name'],
            tech_category= tech['categoryName']
        )
        tech_list.append(new_tech)


for tech in tech_list:
    print(asdict(tech))
