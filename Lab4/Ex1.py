#string manipulation examples

first = input("enter your first name: ")
middleIn = input("enter your middle initial: ")
last = input("enter your last name: ")  

full_name = first + " " + middleIn + ". " + last
print("Your full name is: ", full_name)

print(f"Your full name is: {first} {middleIn}. {last}")

def format_name(first, middle, last):
    full_name = "%s %s. %s" % (first, middle, last)
    return full_name

first = input("Enter first name: ")
middle = input("Enter middle initial: ")
last = input("Enter last name: ")

full_name = "{} {}. {}".format(first, middle, last)

print(full_name)

first = input("Enter first name: ")
middle = input("Enter middle initial: ")
last = input("Enter last name: ")

full_name = " ".join([first, middle + ".", last])

names = [
    input("Enter first name: "),
    input("Enter middle initial: "),
    input("Enter last name: ")
]

full_name = "{} {}. {}".format(*names)

print(full_name)
