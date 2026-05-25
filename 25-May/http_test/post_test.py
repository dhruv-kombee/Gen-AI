import requests

data = {
    "title" : "My post",
    "body" : "Hello World",
    "UseID" : 1
}

res = requests.post("https://jsonplaceholder.typicode.com/posts" , json=data)
print(res.status_code)
print(res.json())


