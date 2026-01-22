#ask the user to enter a floating point number. square the number.
#print the original number and the squared result.
#name: Dante Saito
# date: Jan 22, 2026

Input_value = input("Please enter a floating point number: ")
float_value = float(Input_value)
squared_value = float_value ** 2

# round the number to 2 decimal places
squared_value = round(squared_value, 2)

print("you entered:", float_value)
print("the value squared is:", squared_value)