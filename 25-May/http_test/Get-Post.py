import requests

data = {
    "title": "Learning APIs",
    "body": "REST APIs are powerful",
    "userId": 1
}

response = requests.post(
    "https://jsonplaceholder.typicode.com/posts",
    json=data
)

print(response.status_code)
print(response.json())

res = requests.get("https://jsonplaceholder.typicode.com/posts/1")
data = res.json()
print(res.status_code)
print(data["title"])
print(data["body"])