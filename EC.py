# Variables
age = 70
weekday = "Tuesday"
matinee = True

# Normal price
price = 14

# Senior discount
if age >= 65:
    price = min(price, 8)

# Tuesday discount
if weekday == "Tuesday":
    price = min(price, 10)

# Matinee pricing
if matinee:
    if age >= 65:
        price = min(price, 5)
    else:
        price = min(price, 8)

# Output
print("Age:", age)
print("Weekday:", weekday)
print("Matinee:", matinee)
print("Ticket price: $", price)
