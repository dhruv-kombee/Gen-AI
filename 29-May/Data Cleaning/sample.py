import pandas as pd

data = {
    "Name": ["Dhruv", "Prit", "Dax", "Krish", "Meet", "Milan", "Hardi", "Sneha"],
    "Age": [19, 28, 29, 32, 45, 26, 21, 29],
    "Salary": [19000, 28000, 29000, 32000, 45000, 26000, 21000, 29000],
    "Performance": [89, 87, 86, 84, 75, 76, 96, 82],
}

print("All Detail : ")
df = pd.DataFrame(data)
print(df)
print(df.describe())
print("====================================")
print("Name and Salary :")
row1 = df[["Name","Salary"]]
print(row1)

print("====================================")
print("Name with more salary then 50000:")


condition = df[df["Salary"] > 28000]
print(condition)
print("====================================")
print("Name with Age > 25 and salary > 28000:")

filter = df[(df['Age'] > 30) & (df['Salary'] > 28000)]
print(filter)
print("====================================")
print("Name with Age > 25 or salary > 28000:")

filter = df[(df['Age'] > 30) | (df['Salary'] > 28000)]
print(filter)

print("====================================")
df["Bonus"] = df['Salary'] * 0.1
print(df)


df.insert(0, "Employee ID :" , [10,20,30,40,50,60,70,80])
print(df)