# parse through the portion of an email address 

email = input("Enter your email address: ")

parts = email.split("@")
username = parts[0]
domain = parts[1]

print("username: ", username)
print("domain: ", domain)

# method 2: useing index() and slicing
at_symbol_index = email.index("@")
username_manual = email[:at_symbol_index]
domain_manual = email[at_symbol_index + 1 :]

print("username (manual): ", username_manual)
print("domain (manual): ", domain_manual)