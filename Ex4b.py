def isLeapYear(year):
    result = "Not a leap year"
    if year % 400 == 0:
        result = "Leap year"
    elif year % 100 == 0:
        result = "Not a leap year"
    elif year % 4 == 0:
        result = "Leap year"
    return result
