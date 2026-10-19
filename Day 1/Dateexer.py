
from datetime import datetime, date, timedelta

# Exercise 1: Get today's date
today = date.today()
print("Today's date:", today)

# Exercise 2: Display date in different formats
print("DD-MM-YYYY:", today.strftime("%d-%m-%Y"))
print("DD/MM/YYYY:", today.strftime("%d/%m/%Y"))
print("Readable date:", today.strftime("%B %d, %Y"))

# Exercise 3: Get the current date and time
now = datetime.now()
print("Current date and time:", now)
print("Current time:", now.strftime("%H:%M:%S"))

# Exercise 4: Extract year, month, and day
print("Year:", today.year)
print("Month:", today.month)
print("Day:", today.day)

# Exercise 5: Add 7 days to today's date
next_week = today + timedelta(days=7)
print("Date after 7 days:", next_week)

# Exercise 6: Calculate difference between two dates
date1 = date(2026, 10, 17)
date2 = date(2026, 12, 25)

difference = date2 - date1
print("Days between dates:", difference.days)

# Exercise 7: Convert a string into a date
date_string = "15-08-2026"
converted_date = datetime.strptime(
    date_string, "%d-%m-%Y"
).date()
print("Converted date:", converted_date)

# Exercise 8: Find the weekday
print("Today is:", today.strftime("%A"))
