prices = [150, 10, 20, 350]

total = 0 
Item_count = 0

for price in prices:
    Item_count += 1
    if Item_count > 2:
        discounted_price = price * 0.9 #apply a 10% discount
    else:
        discounted_price = price
    total += discounted_price
    

rounded_total = round(total, 2)
print(f"total price: {total}")
