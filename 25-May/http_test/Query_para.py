import requests

num = input("Enter the ID of user : ")

res = requests.get(f"https://jsonplaceholder.typicode.com/users/{num}")

data = res.json()
print(data["name"])
print(data["email"])
print(res.status_code)