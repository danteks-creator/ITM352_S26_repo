def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

def multiply(x, y):
    return x * y

def divide(x, y):
    if y == 0:
        return "Error: Cannot divide by zero"
    return x / y

def main():
    print("=== Simple Calculator ===")
    
    while True:
        try:
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))
        except ValueError:
            print("Error: Please enter valid numbers")
            continue
        
        print("\nChoose an operation:")
        print("1. Add")
        print("2. Subtract")
        print("3. Multiply")
        print("4. Divide")
        
        operation = input("Enter operation (1/2/3/4): ")
        
        if operation == '1':
            result = add(num1, num2)
            print(f"\n{num1} + {num2} = {result}")
        elif operation == '2':
            result = subtract(num1, num2)
            print(f"\n{num1} - {num2} = {result}")
        elif operation == '3':
            result = multiply(num1, num2)
            print(f"\n{num1} * {num2} = {result}")
        elif operation == '4':
            result = divide(num1, num2)
            print(f"\n{num1} / {num2} = {result}")
        else:
            print("Error: Invalid operation. Please choose 1, 2, 3, or 4")
        
        again = input("\nDo another calculation? (yes/no): ").lower()
        if again != 'yes' and again != 'y':
            print("Thank you for using the calculator!")
            break

if __name__ == "__main__":
    main()
