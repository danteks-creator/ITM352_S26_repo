country_capital = {
    "Germany": "Berlin",
    "Canada": "Ottawa",
    "England": "London"}

print(country_capital)

print(country_capital["Canada"])
print(country_capital["England"])

country_capital["Italy"] = "Rome"
print(country_capital)

country_capital["Italy"] = "Milan"

print("Germany" in country_capital)
print("Spain" not in country_capital)
print("Korea" in country_capital)
