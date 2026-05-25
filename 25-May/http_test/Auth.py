import requests

headers = {
    "Authorization": "Bearer abc12",
    "Content-Type": "application/json"
}

response = requests.get(
    "https://jsonplaceholder.typicode.com/posts",
    headers=headers
)

print(response.status_code)