favorite_celebrities = ("Taylor Swift", "Lionel Messi", "The Weeknd", "Keanu Reeves", "Angelina Jolie")
celebrity_ages = (36, 38, 36, 61, 50)

user_celebrity = input("Enter your favorite celebrity: ")
user_age = int(input("Enter their age: "))

# Convert tuples to lists, append, then convert back to tuples
celebrities_list = list(favorite_celebrities)
ages_list = list(celebrity_ages)

celebrities_list.append(user_celebrity)
ages_list.append(user_age)

updated_celebrities = tuple(celebrities_list)
updated_ages = tuple(ages_list)

print("Updated celebrities tuple:", updated_celebrities)
print("Updated ages tuple:", updated_ages)