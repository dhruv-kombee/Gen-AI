import requests

res = requests.get("https://jsonplaceholder.typicode.com/users")

print(res.status_code)
#print(res.json())


resp = requests.get("https://jsonplaceholder.typicode.com/users/1")

data = resp.json()

print(data["name"])
print(data["email"])