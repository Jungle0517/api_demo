import requests

url = "https://dog.ceo/api/breeds/image/random"

payload = {}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)