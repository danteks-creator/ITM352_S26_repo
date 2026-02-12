# Create a list of lists with test cases for each possible condition

test_cases = [
    ([1, "hello", 3.14, True], "Fewer than 5 elements"),
    ([10, 20, 30, 40, 50, 60, 70], "Between 5 and 10 elements"),
    (["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m"], "More than 10 elements"),
    ([100, 200, 300, 400, 500], "Exactly 5 elements (boundary)"),
    (list(range(1, 11)), "Exactly 10 elements (boundary)"),
    ([1, 2], "2 elements"),
    ([1, 2, 3, 4, 5, 6, 7, 8, 9], "9 elements"),
]

# Test each case
print("Testing list length conditions:\n")
print("-" * 80)

for test_list, description in test_cases:
    length = len(test_list)
    print(f"Test: {description}")
    print(f"List: {test_list}")
    print(f"Length: {length}")
    
    # Control logic to check list length
    if length < 5:
        message = "Fewer than 5 elements"
    elif 5 <= length <= 10:
        message = "Between 5 and 10 elements (inclusive)"
    else:
        message = "More than 10 elements"
    
    print(f"Result: {message}")
    print("-" * 80)
