health = 100

while health > 0:
    print(f"Your health is {health}.")
    damage = int(input("Enter the damage you took: "))
    health -= damage

print("Game Over! Your health has reached zero.")
