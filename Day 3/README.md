# Day 3 — Web Scraping and Data Cleaning

## 1. Project Overview

This project is part of the Linkific Data Engineer Intern training program. It focuses on web scraping, extracting structured information from web pages, collecting datasets, handling errors, and cleaning data using Python.

The practice website used is Books to Scrape, a demonstration bookstore designed for scraping practice.

Website: https://books.toscrape.com/

## 2. Learning Objectives

- Understand web scraping using Python.
- Send HTTP requests and retrieve web pages.
- Parse HTML using BeautifulSoup.
- Extract page titles, links, headings, and book information.
- Practice scraping content rendered by JavaScript using Selenium.
- Collect datasets from multiple pages.
- Clean and validate collected data using pandas.
- Handle request failures and HTTP errors.
- Understand ethical and responsible scraping practices.

## 3. Technologies Used

- Python
- Requests
- BeautifulSoup4
- Selenium
- pandas
- CSV
- Visual Studio Code
- Git and GitHub

## 4. Project Structure

```text
Day 3/
├── scrape_titles.py
├── scrape_links.py
├── scrape_headings.py
├── selenium_dynamic_scraper.py
├── scrape_datasets.py
├── data_cleaning.py
├── ethical_scraping_check.py
├── ethical_scraping_checklist.md
├── requirements.txt
├── README.md
└── data/
    ├── books_main.csv
    ├── books_fiction.csv
    ├── books_travel.csv
    ├── scraping_summary.csv
    ├── books_cleaned.csv
    └── cleaning_report.txt
```

Note: This structure shows the expected files. Only include files and datasets that actually exist in your repository.

## 5. Installation and Setup

### Prerequisites

- Python 3.10 or later
- Visual Studio Code
- Git

### Install Dependencies

Open the terminal in the project root directory and run:

```bash
python -m pip install -r "Day 3/requirements.txt"
```

If the requirements file is not available, install the required packages:

```bash
python -m pip install requests beautifulsoup4 selenium pandas
```

Selenium may require a compatible browser and driver setup depending on the installed Selenium version and browser environment.

## 6. How to Run the Scripts

Run the following commands from the project root directory in PowerShell.

### Extract Page Titles

```powershell
python ".\Day 3\scrape_titles.py"
```

### Extract Links

```powershell
python ".\Day 3\scrape_links.py"
```

### Extract Headings

```powershell
python ".\Day 3\scrape_headings.py"
```

### Scrape JavaScript-Rendered Content

```powershell
python ".\Day 3\selenium_dynamic_scraper.py"
```

### Collect Datasets

```powershell
python ".\Day 3\scrape_datasets.py"
```

This script is intended to collect book information from three pages on Books to Scrape and save the datasets in the `data` folder.

### Clean the Dataset

```powershell
python ".\Day 3\data_cleaning.py"
```

This script is intended to remove duplicate rows, normalize text fields, convert prices into numeric values, and generate a cleaning report.

### Run Ethical Scraping Checks

```powershell
python ".\Day 3\ethical_scraping_check.py"
```

This script checks robots.txt guidance where available, tests page requests, reports HTTP status codes, and counts book listings. Website terms, privacy, redistribution rights, and CSV quality still require appropriate review.

## 7. Dataset Description

| File | Purpose |
|---|---|
| `books_main.csv` | Book data from the main page |
| `books_fiction.csv` | Book data from the Fiction category |
| `books_travel.csv` | Book data from the Travel category |
| `scraping_summary.csv` | Summary of collection results |
| `books_cleaned.csv` | Cleaned book dataset |
| `cleaning_report.txt` | Summary of data cleaning results |

These files are expected outputs. Confirm that each file has been generated before treating it as a completed deliverable.

## 8. Error Handling and Reliability

The scripts may use the following techniques:

- Request timeouts to prevent indefinite waiting.
- Exception handling for connection and HTTP errors.
- HTTP status checks.
- Delays between repeated requests.
- Validation of extracted data.
- Reports for missing or duplicate values.

## 9. Ethical Web Scraping Guidelines

Before scraping:

1. Review the website's robots.txt file.
2. Review available terms and usage information.
3. Collect only necessary, publicly accessible information.
4. Use reasonable request rates and timeouts.
5. Do not bypass access controls or website restrictions.
6. Avoid collecting private or sensitive information.
7. Review data quality before using the datasets.
8. Confirm that collected data can be redistributed before publishing it publicly.

Website robots.txt:
https://books.toscrape.com/robots.txt

## 10. Learning Outcomes

Through this project, I practiced:

- Sending HTTP requests using Python.
- Parsing HTML with BeautifulSoup.
- Extracting structured web content.
- Working with JavaScript-rendered pages using Selenium.
- Collecting and storing data in CSV format.
- Cleaning datasets using pandas.
- Handling errors and validating extracted data.
- Documenting responsible web scraping practices.

## 11. Project Status

Project: Linkific Data Engineer Intern Training  
Module: Web Scraping and Data Cleaning  
Day: Day 3

Status: Update this section after testing the scripts and confirming the expected outputs.

## 12. Author

Prepared as part of the Linkific Data Engineer Intern training program.
