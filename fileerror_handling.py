
import os

filename = "sample.txt"

# Example 1: Handle a missing file
try:
    with open(filename, "r", encoding="utf-8") as file:
        content = file.read()
        print("File content:")
        print(content)

except FileNotFoundError:
    print(f"Error: '{filename}' does not exist.")

except PermissionError:
    print(f"Error: Permission denied for '{filename}'.")

except OSError as error:
    print(f"File operation failed: {error}")


# Example 2: Create and write to a file
try:
    with open("output.txt", "w", encoding="utf-8") as file:
        file.write("Python file handling practice\n")
        file.write("Error handling is important in data engineering.\n")

    print("Data written successfully.")

except OSError as error:
    print(f"Could not write to file: {error}")


# Example 3: Read the newly created file
try:
    with open("output.txt", "r", encoding="utf-8") as file:
        print("\nOutput file contents:")
        print(file.read())

except FileNotFoundError:
    print("Error: Output file was not found.")

except OSError as error:
    print(f"Could not read file: {error}")
