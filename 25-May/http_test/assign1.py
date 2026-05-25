import requests

num = int(input("Enter the ID of the User : "))

res = requests.get(f"https://jsonplaceholder.typicode.com/users/{num}")

data = res.json()

print(data["id"])
print(data["name"])
print(data["email"])
print(res.status_code)