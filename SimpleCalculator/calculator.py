def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        return "Error: Division by zero"
    return a / b

if __name__ == "__main__":
    print("Simple Calculator")
    print("1. Add: 5 + 3 =", add(5, 3))
    print("2. Subtract: 10 - 4 =", subtract(10, 4))
    print("3. Multiply: 3 * 7 =", multiply(3, 7))
    print("4. Divide: 8 / 2 =", divide(8, 2))
    print("5. Divide by zero:", divide(5, 0)) 