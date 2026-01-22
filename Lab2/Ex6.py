#ask the user to enter their weight in pounds.
#convert the weight to kilograms (1 pound = 0.453592 kilograms).
#name: Dante Saito
#date: Jam 22, 2026

kg_to_pounds = 0.453592

weight_in_pounds = input("Enter your weight in pounds: ")
weight_in_pounds_float = float(weight_in_pounds)
weight_in_kg = weight_in_pounds_float * kg_to_pounds
weight_in_kg_rounded = round(weight_in_kg)

print("You entered", weight_in_pounds_float,)
print("Your weight in kilograms is:", weight_in_kg_rounded)
