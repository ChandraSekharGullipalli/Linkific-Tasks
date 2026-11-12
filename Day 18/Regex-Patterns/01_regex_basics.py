
import re

# 1. Literal Characters
text = "Python is a programming language"
print("\n1. Literal Characters:")
print(re.findall("Python", text))

# 2. Metacharacters (.)
text = "cat bat rat mat"
print("\n2. Metacharacters:")
print(re.findall(".at", text))

# 3. Character Classes
text = "apple banana orange mango"
print("\n3. Character Classes:")
print(re.findall("[aeiou]", text))

# 4. Quantifiers (*)
text = "color colour colouur"
print("\n4. Zero or More Characters:")
print(re.findall("colou*r", text))

# 5. Quantifiers (+)
text = "a aa aaa b bb"
print("\n5. One or More Characters:")
print(re.findall("a+", text))

# 6. Quantifiers (?)
text = "color colour"
print("\n6. Optional Characters:")
print(re.findall("colou?r", text))

# 7. Exact Number of Characters
text = "123 1234 12345"
print("\n7. Exact Three Digits:")
print(re.findall(r"\d{3}", text))

# 8. Anchors (^)
text = "Python is easy"
print("\n8. Starting Anchor:")
print(re.findall("^Python", text))

# 9. Anchors ($)
text = "Learn Python"
print("\n9. Ending Anchor:")
print(re.findall("Python$", text))

# 10. Groups
text = "2026-11-12"
print("\n10. Groups:")
result = re.search(r"(\d{4})-(\d{2})-(\d{2})", text)
if result:
    print("Year:", result.group(1))
    print("Month:", result.group(2))
    print("Day:", result.group(3))

# 11. OR Operator (|)
text = "Python Java SQL"
print("\n11. OR Operator:")
print(re.findall("Python|Java", text))

# 12. Word Boundary
text = "cat category cats"
print("\n12. Word Boundary:")
print(re.findall(r"\bcat\b", text))

