
import pandas as pd
from pathlib import Path

# Get the Day 6 folder path
day6_folder = Path(__file__).parent.parent
data_folder = day6_folder / "data"
output_folder = day6_folder / "Output"

# Read CSV files
employees = pd.read_csv(data_folder / "employees.csv")
departments = pd.read_csv(data_folder / "departments.csv")
sales = pd.read_csv(data_folder / "sales.csv")

# Merge employees and departments
employee_details = pd.merge(
    employees, departments,
    on="DepartmentID",
    how="left"
)

# Merge the result with sales
merged_data = pd.merge(
    employee_details, sales,
    on="EmployeeID",
    how="left"
)

# Save the result
output_folder.mkdir(parents=True, exist_ok=True)
merged_data.to_csv(
    output_folder / "merged_employee_sales.csv",
    index=False
)

print("Three-table merge completed!")
print(merged_data)
print("\nSaved to:", output_folder / "merged_employee_sales.csv")
