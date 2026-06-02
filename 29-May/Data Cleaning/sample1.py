import pandas as pd

data = {
    "Name": ["Dhruv", "Prit", "Dax", "Krish", "Meet", "Milan", "Hardi", "Sneha"],
    "Age": [19, 28, 29, 32, 45, 26, 21, 29],
    "Salary": [19000, 28000, 29000, 32000, 45000, 26000, 21000, 29000],
    "Performance": [89, 87, 86, 84, 75, 76, 96, 82],
}

df = pd.DataFrame(data)

#eid = int(input("Enetr the Employee ID : "))
#sal = int(input("Enter the new salary : "))
#df.loc[(eid-1), 'Salary'] = sal

#incresing salary by 5%
df['Salary'] = df['Salary'] * 1.05

print("All Detail : ")
print(df)
