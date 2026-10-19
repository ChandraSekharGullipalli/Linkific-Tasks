
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

url = "https://jsonplaceholder.typicode.com/posts/1"

# Configure retry logic
retry_strategy = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["GET"]
)

adapter = HTTPAdapter(max_retries=retry_strategy)

session = requests.Session()
session.mount("https://", adapter)

try:
    print("Calling API...")

    response = session.get(url, timeout=10)
    response.raise_for_status()

    data = response.json()

    print("API request successful!")
    print("Post ID:", data["id"])
    print("Title:", data["title"])

except requests.exceptions.Timeout:
    print("Error: The API request timed out.")

except requests.exceptions.HTTPError as error:
    print("HTTP error:", error)

except requests.exceptions.ConnectionError:
    print("Error: Could not connect to the API.")

except requests.exceptions.RequestException as error:
    print("Unexpected API error:", error)

finally:
    session.close()
