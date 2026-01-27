#this program demonstrates the use of variable scoping in Python
#name: Dante Saito
#date: Jan 27, 2026

def calculate_discounted_price(price):
    price = price * discount
    print("Inside the function, discounted price is:{price:.2f}")
    return price

discount = 0.6
price = 100 
print(f"Original price before function call is: {price:.2f}")
discounted_price = calculate_discounted_price(price)

print(f"Original price after function call is: {price:.2f}")
print(f"discount=", discount)
