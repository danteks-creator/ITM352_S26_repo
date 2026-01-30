import HandyMath

number1 = float(input("Enter the first number: "))
number2 = float(input("Enter the second number: "))

mid = HandyMath.calculate_midpoint(number1, number2)
print(f"The midpoint between {number1} and {number2} is {mid}")

exp = HandyMath.exponentiate(number1, number2, 3)
print(f"{number1} raised to the power of {number2} is approximately {exp}")

max_value = HandyMath.find_max(number1, number2)
print(f"The maximum between {number1} and {number2} is {max_value}")

min_value = HandyMath.find_min(number1, number2)
print(f"The minimum between {number1} and {number2} is {min_value}") 

sqrt1 = HandyMath.calculate_square_root(number1)
print(f"The square root of {number1} is approximately {sqrt1}")

from HandyMath import max, min 
max_value2 = max(number1, number2)
min_value2 = min(number1, number2)
print(f"(Using direct import) The maximum between {number1} and {number2} is {max_value2}")
print(f"(Using direct import) The minimum between {number1} and {number2} is {min_value2}")

#add a function that takes two numbers x,y and a function name as arguments.
#then it returns a string
def apply_function_and_describe(x, y, func):
    result = func(x, y)
    return f"The result of applying the function to {x} and {y} is {result}"
description = apply_function_and_describe(number1, number2, HandyMath.calculate_midpoint)
print(description)
