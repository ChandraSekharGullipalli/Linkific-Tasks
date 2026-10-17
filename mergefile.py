
import pandas as pd

df1 = pd.read_csv("Employee1.csv")
df2 = pd.read_csv("Employee2.csv")

merged_df = pd.concat([df1, df2], ignore_index=True)

merged_df.to_csv("merged_Employee.csv", index=False)

print("CSV files merged successfully!")
print(merged_df)
