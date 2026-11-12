
import re

# Sample text
text = "Python is easy. Python is powerful. Learn Python."

# 1. re.search()
print("\n1. re.search()")
result = re.search("Python", text)
if result:
    print("Found:", result.group())
    print("Position:", result.start())

# 2. re.match()
print("\n2. re.match()")
result = re.match("Python", text)
if result:
    print("Matched:", result.group())
else:
    print("No match found")

# 3. re.findall()
print("\n3. re.findall()")
result = re.findall("Python", text)
print("All matches:", result)

# 4. re.sub()
print("\n4. re.sub()")
result = re.sub("Python", "Java", text)
print(result)

# 5. re.compile()
print("\n5. re.compile()")
pattern = re.compile(r"\d+")
numbers = pattern.findall("Order 101, Product 202, Bill 303")
print("Numbers:", numbers)

# 6. Case-insensitive flag
print("\n6. IGNORECASE Flag")
text = "Python PYTHON python"
result = re.findall("python", text, re.IGNORECASE)
print(result)

# 7. MULTILINE Flag
print("\n7. MULTILINE Flag")
text = """Python is easy
Java is popular
Python is powerful"""
result = re.findall(r"^Python", text, re.MULTILINE)
print(result)

# 8. DOTALL Flag
print("\n8. DOTALL Flag")
text = "Hello\nPython"
result = re.findall(r"Hello.Python", text, re.DOTALL)
print(result)

# 9. re.split()
print("\n9. re.split()")
text = "Apple, Banana; Orange Mango"
result = re.split(r"[,; ]+", text)
print(result)

# 10. re.fullmatch()
print("\n10. re.fullmatch()")
email = "student@gmail.com"
result = re.fullmatch(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", email)
print("Valid email" if result else "Invalid email")

