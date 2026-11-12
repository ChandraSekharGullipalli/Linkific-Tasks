
import re
import pandas as pd
from pathlib import Path
from collections import Counter

# Project paths
BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "data" / "sample.log"
OUTPUT_DIR = BASE_DIR / "outputs"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Read log file
with open(INPUT_FILE, "r", encoding="utf-8") as file:
    log_lines = file.readlines()

print("\n1. Total Log Lines:", len(log_lines))

# Compile regex pattern
log_pattern = re.compile(
    r"^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})"
    r"\s+(INFO|WARNING|ERROR|DEBUG)"
    r"\s+(.+)$"
)

# Parse logs
records = []
invalid_lines = []

for line_number, line in enumerate(log_lines, start=1):

    line = line.strip()

    if not line:
        continue

    match = log_pattern.fullmatch(line)

    if match:
        timestamp, level, message = match.groups()

        records.append({
            "LineNumber": line_number,
            "Timestamp": timestamp,
            "LogLevel": level,
            "Message": message
        })

    else:
        invalid_lines.append({
            "LineNumber": line_number,
            "RawLog": line
        })

# Create DataFrame
df = pd.DataFrame(records)

print("\n2. Successfully Parsed Logs:")
print(df.to_string(index=False))

# Count log levels
print("\n3. Log Level Statistics:")

if not df.empty:
    log_counts = Counter(df["LogLevel"])

    for level, count in sorted(log_counts.items()):
        print(f"{level}: {count}")

# Extract errors
print("\n4. Error Analysis:")

errors = df[df["LogLevel"] == "ERROR"]

for error in errors["Message"]:
    print("-", error)

# Extract warnings
print("\n5. Warning Analysis:")

warnings = df[df["LogLevel"] == "WARNING"]

for warning in warnings["Message"]:
    print("-", warning)

# Extract timestamps
print("\n6. Timestamp Extraction:")

timestamps = re.findall(
    r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}",
    "\n".join(log_lines)
)

print("Total timestamps:", len(timestamps))

# Search database-related messages
print("\n7. Database Related Logs:")

database_logs = df[
    df["Message"].str.contains(
        "database",
        case=False,
        na=False
    )
]

print(database_logs.to_string(index=False))

# Save parsed logs
df.to_csv(OUTPUT_DIR / "advanced_parsed_logs.csv", index=False)

# Save error report
errors.to_csv(OUTPUT_DIR / "advanced_error_report.csv", index=False)

# Save warning report
warnings.to_csv(OUTPUT_DIR / "advanced_warning_report.csv", index=False)

# Save invalid logs
pd.DataFrame(invalid_lines).to_csv(
    OUTPUT_DIR / "invalid_logs.csv",
    index=False
)

# Save summary report
summary = (
    df["LogLevel"]
    .value_counts()
    .rename_axis("LogLevel")
    .reset_index(name="Count")
)

summary.to_csv(OUTPUT_DIR / "advanced_log_summary.csv", index=False)

# Final statistics
print("\n8. Final Log Analysis:")
print("Total lines:", len(log_lines))
print("Parsed records:", len(df))
print("Invalid records:", len(invalid_lines))
print("Error records:", len(errors))
print("Warning records:", len(warnings))

print("\n9. Generated Files:")
print("advanced_parsed_logs.csv")
print("advanced_error_report.csv")
print("advanced_warning_report.csv")
print("invalid_logs.csv")
print("advanced_log_summary.csv")

