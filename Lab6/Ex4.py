"""
Leap Year Program with Structured Conditional Logic

Leap Year Rules:
- A year is a leap year if:
  * (Condition A AND Condition B) OR Condition C
  * (Divisible by 4 AND NOT divisible by 100) OR (Divisible by 400)

Why Parentheses Matter:
  - Without explicit grouping, operator precedence could cause confusion
  - Python gives AND higher precedence than OR, but explicit parentheses make intent clear
  - The structure (A AND B) OR C ensures: "leap if divisible by 4 but not 100, OR if divisible by 400"
"""

def is_leap_year(year):
    """
    Determine if a year is a leap year using the structured conditional logic:
    (Condition A AND Condition B) OR Condition C
    
    Condition A: year % 4 == 0        (divisible by 4)
    Condition B: year % 100 != 0      (NOT divisible by 100)
    Condition C: year % 400 == 0      (divisible by 400)
    """
    # Explicit parentheses ensure correct evaluation order and match flowchart
    if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
        return True
    else:
        return False


def print_leap_year_analysis(year):
    """Print detailed breakdown of leap year calculation."""
    is_leap = is_leap_year(year)
    
    print(f"\n{'='*60}")
    print(f"Year: {year}")
    print(f"{'='*60}")
    print(f"Condition A: {year} % 4 == 0?        → {year % 4 == 0}")
    print(f"Condition B: {year} % 100 != 0?      → {year % 100 != 0}")
    print(f"Condition C: {year} % 400 == 0?      → {year % 400 == 0}")
    print(f"\n(Condition A AND Condition B) OR Condition C")
    print(f"({year % 4 == 0} AND {year % 100 != 0}) OR {year % 400 == 0}")
    print(f"({year % 4 == 0 and year % 100 != 0}) OR {year % 400 == 0}")
    print(f"= {is_leap}")
    
    if is_leap:
        print(f"\n✓ {year} is a LEAP YEAR (February has 29 days)")
    else:
        print(f"\n✗ {year} is NOT a leap year (February has 28 days)")


# ============================================================
# TEST WITH YOUR BIRTH YEAR AND CLOSEST LEAP YEAR
# ============================================================

# MODIFY THESE VALUES WITH YOUR OWN INFORMATION:
your_birth_year = 2000  # Example: replace with your actual birth year
non_leap_year = 2001    # Example: replace with closest non-leap year to your birth

print("\n" + "="*60)
print("LEAP YEAR TESTING WITH BIRTH YEAR")
print("="*60)

print("\n📅 BIRTH YEAR TEST:")
print_leap_year_analysis(your_birth_year)

print("\n📅 CLOSEST NON-LEAP YEAR TEST:")
print_leap_year_analysis(non_leap_year)

# ============================================================
# ADDITIONAL BOUNDARY TEST CASES
# ============================================================

print("\n\n" + "="*60)
print("BOUNDARY TEST CASES (Verification)")
print("="*60)

boundary_years = [
    (1900, False, "Divisible by 100 but NOT 400 → NOT leap"),
    (2000, True,  "Divisible by 400 → leap"),
    (2004, True,  "Divisible by 4, NOT by 100 → leap"),
    (2001, False, "NOT divisible by 4 → NOT leap"),
    (2100, False, "Divisible by 100 but NOT 400 → NOT leap"),
]

for year, expected, description in boundary_years:
    result = is_leap_year(year)
    status = "✓" if result == expected else "✗"
    print(f"{status} {year}: {result:5} | {description}")

print("\n" + "="*60)
print("INSTRUCTIONS FOR YOUR SUBMISSION:")
print("="*60)
print("1. Replace 'your_birth_year = 2000' with YOUR actual birth year")
print("2. If your birth year IS a leap year:")
print("   - Set non_leap_year = your_birth_year + 1")
print("3. If your birth year is NOT a leap year:")
print("   - Keep non_leap_year = the closest leap year to your birth year")
print("="*60)

