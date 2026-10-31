import os
from extract_csv import extract_hospital_data
from extract_api import extract_api_data
from extract_json import extract_json_data


def main():

    print("\n========== MULTI-SOURCE EXTRACTION STARTED ==========\n")

    # Create output folder if it does not exist
    os.makedirs("output", exist_ok=True)

    # 1. Extract CSV data
    print("\n--- CSV EXTRACTION ---")
    patients = extract_hospital_data()

    # 2. Extract API data
    print("\n--- API EXTRACTION ---")
    posts = extract_api_data()

    # 3. Extract JSON data
    print("\n--- JSON EXTRACTION ---")
    courses = extract_json_data()

    # Save extracted datasets
    if patients is not None:
        patients.to_csv("output/hospital_patients_extracted.csv", index=False)
        print("\nHospital data saved successfully!")

    if posts is not None:
        posts.to_csv("output/api_posts_extracted.csv", index=False)
        print("API data saved successfully!")

    if courses is not None:
        courses.to_csv("output/online_courses_extracted.csv", index=False)
        print("Course data saved successfully!")

    print("\n========== EXTRACTION SUMMARY ==========")

    print("Hospital records:", len(patients) if patients is not None else 0)
    print("API records:", len(posts) if posts is not None else 0)
    print("Course records:", len(courses) if courses is not None else 0)

    print("\n========== MULTI-SOURCE EXTRACTION COMPLETED ==========")


if __name__ == "__main__":
    main()