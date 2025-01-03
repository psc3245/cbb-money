def americanToMultiplier(odds) -> float:
    if (odds[0] == "+"):
        return 1.0 + (float(odds[1:]) / 100)
    if (odds[0] == "-"):
        return 1.0 + (100.0 / float(odds[1:]))

def americanToImpliedProb(odds) -> float:
    num = int(odds[1:])
    if (odds[0] == "+"):
        return 100 / (num + 100)
    if (odds[0] == "-"):
        return  num / (100.0 + num)

def calculateHold(bet, oddsA, oddsB) -> float:
    multiplerA = americanToMultiplier(oddsA)
    multiplerB = americanToMultiplier(oddsB)

    impliedProbA = americanToImpliedProb(oddsA)
    impliedProbB = americanToImpliedProb(oddsB)

    impliedProbSum = impliedProbA + impliedProbB

    # print(f"Probability Summary: \n   Implied probability A: {impliedProbA} \n   Implied probability B: {impliedProbB} \n   Implied probability total: {impliedProbSum}")

    if (impliedProbSum < 1.0):

        toBetA = impliedProbA / impliedProbSum * bet
        if (toBetA - int(toBetA) < 0.5): 
            toBetA_rounded = int(toBetA)
        else:
            toBetA_rounded = int(toBetA) + 1

        profitA = toBetA * multiplerA - bet
        profitA_rounded = toBetA_rounded * multiplerA - bet

        toBetB = impliedProbB / impliedProbSum * bet
        if (toBetB - int(toBetB) < 0.5): 
            toBetB_rounded = int(toBetB)
        else:
            toBetB_rounded = int(toBetB) + 1

        profitB = toBetB * multiplerB - bet
        profitB_rounded = toBetB_rounded * multiplerB - bet

        print("Rounded Betting:")
        print(f" - A rounded ${toBetA_rounded:.2f} bet on {oddsA} will yield {profitA_rounded:.2f}")
        print(f" - A rounded ${toBetB_rounded:.2f} bet on {oddsB} will yield {profitB_rounded:.2f}")
        print(f"Calculated {((profitA_rounded + profitB_rounded) / (bet * 2) * 100):.2f}% average hold on this opportunity. \n")

        print("True Arbitrage Betting:")
        print(f" - A ${toBetA:.2f} bet on {oddsA} will yield {profitA:.2f}")
        print(f" - A ${toBetB:.2f} bet on {oddsB} will yield {profitB:.2f}")
        print(f"Calculated {((profitA + profitB) / (bet * 2) * 100):.2f}% hold on this opportunity.")

    else:
        print(f"Odds {oddsA} and {oddsB} is NOT an arbitrage opportunity.")


keepgoing = True

while (keepgoing):
    bet = int(input("How Much To Bet: "))
    oddsA = input("Site A Odds: ")
    oddsB = input("Site B Odds: ")

    print()
    print("Results: ")
    print("----------------------------")

    calculateHold(bet, oddsA, oddsB)

    print("----------------------------")

    keepgoing = (input("Do another bet? (y/n): ") == "y")
    print()

    
        


    
    



