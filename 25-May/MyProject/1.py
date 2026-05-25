import requests

response = requests.get("https://jsonplaceholder.typicode.com/users")

print(response)


#response1 = requests.get("https://jsonplaceholder.typicode.com/users")
#data = response1.json()
#print(data)



response2 = requests.get("https://jsonplaceholder.typicode.com/users")

data = response2.json()

print(data[0]["name"])


