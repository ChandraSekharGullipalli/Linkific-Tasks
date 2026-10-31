import pandas as pd

def extract_hospital_data():
    file_path = "Data/hospital_patients.csv"

    patients = pd.read_csv(file_path)

    print("CSV Extraction Successful!")
    print("Total patient records:", len(patients))
    print("\nPatient Data:")
    print(patients.head())

    return patients


if __name__ == "__main__":
    extract_hospital_data()