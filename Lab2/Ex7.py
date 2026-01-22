#ask the user to enter a temperature in farenheit.
#convert the temperature to celsius using the formula: (F - 32) * 5/9
#name: Dante Saito
#date: Jan 22. 2026

farenheit_input = input("Please enter a temperature in Fahrenheit: ")
farenheit_value = float(farenheit_input)
celsius = (farenheit_value - 32) * 5/9
celsius_value_rounded = round(celsius, 1)

print("You entered:", farenheit_value)
print("The temperature in Celsius is:", celsius_value_rounded)