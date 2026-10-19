## Linkific-Tasks
Daily training tasks and deliverables for my Data Engineer Internship at Linkific
 Linkific Day 1 – Python for Data Engineering

## Project Overview

This repository contains my Day 1 learning tasks and practical exercises for the Data Engineer Intern role at Linkific. The objective is to build a strong foundation in Python, configure a professional development environment, and practice essential programming concepts used in data engineering.

## Learning Objectives

- Set up a Python development environment on Windows 11.
- Configure VS Code, Git, and GitHub for development and version control.
- Practice Python fundamentals and data structures.
- Work with files using Python.
- Read and process CSV, JSON, and text files.
- Practice date and time manipulation using Python's `datetime` module.
- Document the project setup and execution instructions.

## Technologies and Tools

- **Python** – Programming and data processing
- **Visual Studio Code** – Code editor
- **Git** – Version control
- **GitHub** – Repository hosting and project sharing
- **Windows 11** – Development environment

## Project Structure

The repository is organized to keep the Python exercises and file-processing examples easy to understand and maintain.

```text
linkific-day1-python/
│
├── python_basics/
│   ├── variables.py
│   ├── data_types.py
│   ├── operators.py
│   ├── conditional_statements.py
│   └── loops.py
│
├── data_structures/
│   ├── lists.py
│   ├── tuples.py
│   ├── dictionaries.py
│   └── sets.py
│
├── file_handling/
│   ├── text_file_example.py
│   ├── csv_file_example.py
│   └── json_file_example.py
│
├── datetime_examples/
│   ├── current_datetime.py
│   ├── date_formatting.py
│   └── date_difference.py
│
├── README.md
└── .gitignore
```

*Note: This is a suggested structure. Keep only the files and folders that you have actually created in your repository.*

## Environment Setup

### 1. Install Python

Download Python from the official website:

https://www.python.org/downloads/

Verify the installation in the VS Code terminal:

```bash
python --version
```

If that command does not work on Windows, try:

```bash
py --version
```

### 2. Install Visual Studio Code

Download VS Code:

https://code.visualstudio.com/

Install the Python extension published by Microsoft and open your project folder in VS Code.

### 3. Install and Configure Git

Download Git:

https://git-scm.com/downloads

Verify the installation:

```bash
git --version
```

Configure your Git identity:

```bash
git config --global user.name "Your Name"
git config --global user.email "your-email@example.com"
```

Replace the example values with your own details.

### 4. Configure GitHub

Create a repository on GitHub and connect your local project folder to it. Use the repository URL provided by GitHub.

## Python Practice Tasks

### Python Fundamentals

Practice variables, data types, operators, conditional statements, loops, and functions through small Python programs.

### Data Structures

Practice using:

- Lists to store collections of values.
- Tuples for ordered, immutable collections.
- Dictionaries to store key-value pairs.
- Sets to work with unique values.

### File Handling

Practice reading and writing different file formats.

- **Text files:** Read text, write content, and append data.
- **CSV files:** Read rows, access columns, and process tabular data.
- **JSON files:** Load structured data and write Python data as JSON.

### Date and Time Manipulation

Use Python's `datetime` module to:

- Retrieve the current date and time.
- Format dates and timestamps.
- Parse date strings.
- Calculate differences between dates.

## How to Run the Programs

1. Clone the repository or download the project from GitHub.
2. Open the project folder in VS Code.
3. Open the integrated terminal.
4. Navigate to the folder containing the Python script.
5. Run the script using Python.

Example:

```bash
python python_basics/variables.py
```

For file-processing programs, ensure the required input files are available at the paths specified in the code.

## Version Control with Git

Use Git to track project changes and push the work to GitHub.

```bash
git status
git add .
git commit -m "Complete Day 1 Python practice tasks"
git push
```

If this is the first push, configure the remote repository and upstream branch according to your GitHub repository setup.

## Expected Deliverables

- Python development environment configured.
- Python scripts demonstrating fundamental concepts and data structures.
- File-processing examples for CSV, JSON, and text files.
- Date and time manipulation examples.
- Git and GitHub repository configuration.
- README documentation with setup and execution instructions.

## Learning Outcome

This project helps establish the Python programming, file-handling, and development workflow skills required for further data engineering tasks, including data ingestion, transformation, API integration, and pipeline development.

## Author

**Name:** Chandra Sekhar Gullipalli  
**Role:** Data Engineer Intern  
**Organization:** Linkific

**GitHub Repository:** Add your repository URL here.
