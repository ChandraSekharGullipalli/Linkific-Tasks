import requests
import pandas as pd

def extract_api_data():

    url = "https://jsonplaceholder.typicode.com/posts"

    response = requests.get(url, timeout=15)

    if response.status_code == 200:
        data = response.json()

        posts = pd.DataFrame(data)

        print("API Extraction Successful!")
        print("Total records extracted:", len(posts))

        print("\nFirst 5 API Records:")
        print(posts.head())

        return posts

    else:
        print("API request failed!")
        print("Status Code:", response.status_code)
        return None


if __name__ == "__main__":
    extract_api_data()