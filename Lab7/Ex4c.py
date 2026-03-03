def check_purchases_against_budget(recent_purchases, budget):
    messages = []
    for expense in recent_purchases:
        if expense > budget:
            messages.append("This purchase is over budget!")
        else:
            messages.append("This purchase is within budget")
    return messages


if __name__ == "__main__":
    recent_purchases = [36.13, 23.87, 183.35, 22.93, 11.62]
    budget = 50.00

    results = check_purchases_against_budget(recent_purchases, budget)
    for message in results:
        print(message)