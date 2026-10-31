import json
import pandas as pd

def extract_json_data():

    file_path = "Data/online_courses.json"

    with open(file_path, "r") as file:
        data = json.load(file)

    courses = pd.DataFrame(data)

    print("JSON Extraction Successful!")
    print("Total course records:", len(courses))

    print("\nCourse Data:")
    print(courses)

    return courses


if __name__ == "__main__":
    extract_json_data()