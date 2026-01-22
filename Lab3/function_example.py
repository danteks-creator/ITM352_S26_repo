#an example of creating and using your own function.
#name: Dante Saito
#date: Jan 22, 2026
import datetime

def greet(name):
    """This function greets the person whose name is passed as an argument.
    In addition we want to print a welcome message. that includes 
    the day of the week."""
    message = f"Hello," + " " + name + "!"
    x = datetime.datetime.now()
    day_of_week = x.strftime("%A")
    message += f"Happy {day_of_week}."
    return message

user_name = input("Please enter your name: ")
greeting_message = greet(user_name)
print(greeting_message)