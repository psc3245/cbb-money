# Goal: create a small program that takes in two sets of odds and finds the most profitable setup for betting in increments of 50 cents

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
    print("\n")
    print("Probability Summary:")
    print(f"Implied probability A: {impliedProbA}")
    print(f"Implied probability B: {impliedProbB}")
    print(f"Implied probability total: {impliedProbSum}")
    print("\n")


    if (impliedProbSum < 1.0):
        print(f"Odds {oddsA} and {oddsB} is an arbitrage opportunity. \n")

        toBetA = impliedProbA / impliedProbSum * bet
        profitA = toBetA * multiplerA - bet
        print(f"A ${toBetA:.2f} bet on {oddsA} will yield {profitA:.2f}")

        toBetB = impliedProbB / impliedProbSum * bet
        profitB = toBetB * multiplerB - bet
        print(f"A ${toBetB:.2f} bet on {oddsB} will yield {profitB:.2f}")
        print("\n")

        hold = (profitA + profitB) / (bet * 2) * 100
        
        if (profitA == profitB): print(f"Calculated {hold:.2f}% hold on this opportunity.")
        else: print(f"Calculated {hold:.2f}% average hold on this opportunity.")
    else:
        print(f"Odds {oddsA} and {oddsB} is NOT an arbitrage opportunity.")


keepgoing = True

if(keepgoing): #while (keepgoing):
    bet = int(input("How Much To Bet: "))
    oddsA = input("Site A Odds: ")
    oddsB = input("Site B Odds: ")

    calculateHold(bet, oddsA, oddsB)

    
        


    
    



