
import re
import pandas as pd
from pathlib import Path
from collections import Counter


# Define file paths
BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "data" / "sample.log"
OUTPUT_DIR = BASE_DIR / "outputs"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Read log file
with open(INPUT_FILE, "r", encoding="utf-8") as file:
    log_data = file.readlines()

print("\n1. Total Log Records:", len(log_data))

# Compile regex pattern
pattern = re.compile(
    r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) "
    r"(INFO|WARNING|ERROR) (.+)"
)

# Extract log details
records = []

for line in log_data:
    match = pattern.search(line.strip())

    if match:
        timestamp, level, message = match.groups()

        records.append({
            "Timestamp": timestamp,
            "LogLevel": level,
            "Message": message
        })

# Convert records into DataFrame
df = pd.DataFrame(records)

print("\n2. Extracted Log Records:")
print(df.to_string(index=False))

# Count log levels
print("\n3. Log Level Summary:")
log_counts = Counter(df["LogLevel"])

for level, count in log_counts.items():
    print(f"{level}: {count}")

# Extract error messages
print("\n4. Error Messages:")
errors = df[df["LogLevel"] == "ERROR"]

for message in errors["Message"]:
    print("-", message)

# Extract warning messages
print("\n5. Warning Messages:")
warnings = df[df["LogLevel"] == "WARNING"]

for message in warnings["Message"]:
    print("-", message)

# Extract timestamps
print("\n6. Extracted Timestamps:")
timestamps = re.findall(
    r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}",
    "".join(log_data)
)

for timestamp in timestamps:
    print(timestamp)

# Save complete parsed logs
df.to_csv(OUTPUT_DIR / "parsed_logs.csv", index=False)

# Save error logs separately
errors.to_csv(OUTPUT_DIR / "error_logs.csv", index=False)

# Save summary report
summary = pd.DataFrame(
    log_counts.items(),
    columns=["LogLevel", "Count"]
)

summary.to_csv(OUTPUT_DIR / "log_summary.csv", index=False)

print("\n7. Generated Output Files:")
print("parsed_logs.csv")
print("error_logs.csv")
print("log_summary.csv")
