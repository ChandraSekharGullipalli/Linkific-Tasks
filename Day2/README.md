# Day 2 - Python API Integration and Data Collection

## 1. Overview

This project demonstrates how to integrate public REST APIs using Python, retrieve JSON data, handle errors, implement pagination, and save collected data in CSV format.

## 2. Objectives

- Understand REST APIs and HTTP GET requests.
- Retrieve data from public APIs.
- Practice API key and Bearer token authentication.
- Implement error handling and retry logic.
- Retrieve data using pagination.
- Collect API datasets and save them as CSV files.
- Organize Python scripts for data engineering practice.

## 3. Technologies Used

- Python 3
- Requests library
- REST APIs
- JSON
- CSV
- Git
- GitHub
- Visual Studio Code

## 4. Project Structure

```text
Day2/
├── api_weather.py
├── api_users.py
├── api_posts.py
├── api_key_auth.py
├── bearer_token_auth.py
├── api_retry_logic.py
├── api_pagination.py
├── collect_api_dataset.py
├── api_posts_dataset.csv
└── README.md
```

## 5. APIs Used

### JSONPlaceholder

URL: [https://jsonplaceholder.typicode.com/](https://jsonplaceholder.typicode.com/)

Used to retrieve sample user details and blog posts for API integration and data collection practice.

### Open-Meteo

URL: [https://open-meteo.com/](https://open-meteo.com/)

Used to retrieve weather measurements without requiring an API key for the example demonstrated.

### OpenWeatherMap

URL: [https://openweathermap.org/api](https://openweathermap.org/api)

Used to practice API key authentication. A valid API key is required for the weather request.

### HTTPBin

URL: [https://httpbin.org/](https://httpbin.org/)

Used to demonstrate Bearer token authentication with a test endpoint.

## 6. Setup Instructions

### Step 1: Install Python

Install Python 3 and verify the installation:

```bash
python --version
```

### Step 2: Install the Requests Library

```bash
python -m pip install requests
```

### Step 3: Open the Project

Open the `Linkific-Tasks` folder in Visual Studio Code.

### Step 4: Run an API Script

For example:

```powershell
python .\Day2\api_users.py
```

Run other scripts by replacing the filename with the relevant Python file.

## 7. API Collection Guide

### Step 1: Send an API Request

Use `requests.get()` to retrieve data from an API endpoint.

### Step 2: Check the Response

Use `response.raise_for_status()` to detect unsuccessful HTTP responses.

### Step 3: Convert JSON to Python Data

Use `response.json()` to parse the JSON response.

### Step 4: Process the Records

Use Python loops to access fields and process the retrieved records.

### Step 5: Save Data as CSV

Use Python's `csv` module to write the API records into a CSV file.

### Step 6: Verify the Dataset

Open `api_posts_dataset.csv` and check the column names and collected records.

## 8. Error Handling and Retry Logic

The retry script demonstrates:

- Connection error handling
- Timeout handling
- HTTP status validation
- Automatic retries for selected transient failures
- Backoff between retry attempts

## 9. Pagination

The pagination script retrieves records in smaller batches using page and limit parameters. It continues until the API returns no additional records.

## 10. Authentication

The authentication examples demonstrate:

- API key authentication
- Bearer token authentication
- HTTP Authorization headers
- Environment variables
- Basic authentication failure handling

Never commit real API keys, access tokens, or passwords to GitHub.

## 11. Expected Deliverables

- Python API integration scripts
- Authentication examples
- Error handling and retry logic
- Pagination implementation
- API dataset collection script
- CSV dataset
- README documentation

## 12. Learning Outcomes

Practiced integrating APIs with Python, processing JSON responses, handling HTTP errors, implementing pagination, and saving collected data in CSV format.

## 13. Execution Status

Update this section after testing the scripts:

- [x] Weather API tested
- [x] Users API tested
- [x] Posts API tested
- [x] API key authentication tested
- [x] Bearer token example tested
- [x] Retry logic tested
- [x] Pagination tested
- [x] CSV dataset generated and verified

## 14. Author

Linkific Data Engineer Intern Training - Day 2
