import requests
import json

url = "https://api.builtin.com/graphql"

payload = json.dumps({
    "operationName": "GetCompanyTechnologies",
    "query": "query GetCompanyTechnologies($id: Int!) {\n companyByID(id: $id) {\n technologies {\n name\n urlName\n categoryName\n }\n extraTechnologies {\n name\n categoryName\n }\n }\n}\n",
    "variables": {
    "id": 54043
    }
})
headers = {
    'Content-Type': 'application/json',
    'Cookie': '__cf_bm=ZeNfR0EkBcvQlfEIOy1RSpX2Qn62TDVjeo56SI7G_WY-1712182970-1.0.1.1-03XZzLV25fTbcZhcoV.tAX3VeSiWsYYDPL3WjxLqDzJrMh6VdjAe7cwOjVXZE5ZDLmxODnP4c8_BBbD74YTT6A'
}

response = requests.request("POST", url, headers=headers, data=payload)

# watch the rest of the video to find out how to use pandas to easily convert json to csv
print(response.text)
