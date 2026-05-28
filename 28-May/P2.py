import requests

id = int(input("Enter the id : "))
num = requests.get(f"https://api.restful-api.dev/objects/{id}") 
data = num.json()
print(data['name'])

phone = input("Enter the name of the phone : ")
res = requests.get(f"https://api.restful-api.dev/objects?name={phone}")
data1 = res.json()
print(data1['id'])
