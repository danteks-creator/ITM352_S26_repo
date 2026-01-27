#Handy library of exponential and logarithmic math functions
#name: Dante Saito
#date: Jan 27, 2026

from math import exp


def midpoint(x1, y1, x2, y2):
    """Calculate the midpoint between two numbers"""
    mid = (x1 + x2) / 2
    return mid

def sqrt(number):
    """Calculate the square root of a number"""
    if number < 0:
        return None
    return number ** 0.5

def exponent(base, exp, precision):
    """Calculate the exponentiation of a base to a given exponent"""
    result = base ** exp
    rounded_result = round(result, precision)
    return rounded_result