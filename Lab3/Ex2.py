# create a function called midpoint

def midpoint(x1, y1, x2, y2):
    """Calculate the midpoint between two numbers"""
    mid = (number1 + number2) / 2
    return mid

number1 = float(input("Enter first number: "))
number2 = float(input("Enter second number: "))
result = midpoint(number1, number2)
print("The midpoint between, {number1} and {number2} is {result}")
