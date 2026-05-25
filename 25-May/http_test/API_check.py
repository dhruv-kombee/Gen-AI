import requests

url = input("Enter URL: ")

response = requests.get(url)

if response.status_code == 200:
    print("API Working")
else:
    print("API Failed")