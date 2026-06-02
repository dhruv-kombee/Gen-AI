import pandas as pd

data = {
    "Name": ["Dhruv", None, "Dax", "Krish", "Meet", "Milan", "Hardi", "Sneha"],
    "Age": [19, None, 29, 32, 45, 26, 21, 29],
    "Salary": [19000, None, 29000, 32000, 45000, 26000, 21000, 29000],
    "Performance": [89, None, 86, 84, 75, 76, 96, 82]
}

print("All Detail : ")
df = pd.DataFrame(data)
df.drop(columns=['Performance'] , inplace=True)
print(df)
print("\n\n\n")
print(df.isnull())
print(df.isnull().sum())

