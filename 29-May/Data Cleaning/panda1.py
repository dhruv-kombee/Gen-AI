import pandas as pd

data = {
    "name": ["Dhruv" , "Dhruv"],
    "age": [19 , 19]
}

df = pd.DataFrame(data)
print("First")
print(df)
print("Second")
df.head()
print("Third")
print(df['age'])


