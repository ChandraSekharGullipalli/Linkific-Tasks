
# Process application log files

log_file = "app.log"
output_file = "error_logs.txt"

total_lines = 0
error_count = 0
warning_count = 0

with open(log_file, "r", encoding="utf-8") as file:
    logs = file.readlines()

with open(output_file, "w", encoding="utf-8") as output:
    for line in logs:
        total_lines += 1

        if "ERROR" in line:
            error_count += 1
            output.write(line)

        elif "WARNING" in line:
            warning_count += 1

print("Log processing completed!")
print("Total log lines:", total_lines)
print("Errors found:", error_count)
print("Warnings found:", warning_count)
print("Error details saved to:", output_file)
