import random

#Starter Values
money = 5000
_SUITS = ('♥', '♦', '♠', '♣')
_SINGLEDECK = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
deckindex = 0
game = True

#settings -- 0 = False 1 = True
isasking = False # by defould is off. Its just what i think is better.
isInsuranceAsking = True # by default its on.

#Decks:
deckValues = _SINGLEDECK * 4
deckValues = list(deckValues)

deckSuits = (suit for suit in _SUITS for _ in _SINGLEDECK)
deckSuits = list(deckSuits)


# Playing cards:
dealersCards = []
playersCards = []


# formating:
_SPACING = " " * 2
_TOPBORDER = "_" * 3
_BOTTOMBORDER = "_" * 2
_SETTINGS = "What do you want to change?\n" \
            "Name      | Command             | What dose it do. \n" \
            "Asking    | 'a', 'ask', 'asking'| Changes asking if you want to continue.\n" \
            "Insurance | 'I', 'insurance'    | Disables/Enables insurance.\n"


def insuranceAsking():
    global isInsuranceAsking
    while True:
        if isInsuranceAsking == True:
            output = input("Do you want to turn off insurance asking? (Y/N)\n>")
        if isInsuranceAsking == False:
            output = input("Do you want to turn on insurance asking? (Y/N)\n>")
        if output.upper() == "Y":
            isInsuranceAsking = not isInsuranceAsking
            print("Insurance asking changed.")
            return
        elif output.upper() == "N":
            print("Nothing changed.")
            return
        else:
            print("Type 'Y' for yes or 'N' for no!")


def changeAsking():
    global isasking
    while True:
        if isasking == True:
            output = input("Do you want to turn off asking? (Y/N)\n>")
        if isasking == False:
            output = input("Do you want to turn on asking? (Y/N)\n>")
        if output.upper() == "Y":
            isasking = not isasking
            print("Asking changed.")
            return
        elif output.upper() == "N":
            print("Nothing changed.")
            return
        else:
            print("Type 'Y' for yes or 'N' for no!")


def settings():
    global _SETTINGS
    while True:
        print(_SETTINGS)
        output = input(">")
        print(output)
        if output.upper() == "A" or output.upper() == "ASK" or output.upper() == "ASKING":
            changeAsking()
            return
        if output.upper() == "I" or output.upper() == "INSURANCE":
            insuranceAsking()
            return


def deckShuffle():
    deck = list(zip(deckValues, deckSuits))
    random.shuffle(deck)
    deck.append(("#", "#"))
    return deck


def gameStart(money):
    while True:
        print(f"\nYou have {money} coins")
        bet = input(f"How much do you bet? (1-{money}, quit or setting)\n>")
        try:
            bet = int(bet)
            if bet >= 1 and bet <= money:
                return bet
            else:
                print(f"Please enter a number between 1 and {money}.")
        except:
            if bet.upper() == "QUIT":
                exit(0)
            elif bet.upper() == "SETTING" or bet.upper() == "SETTINGS" or bet.upper() == "SET":
                settings()
                continue
            print("Error: Please enter a valid number or 'QUIT' to exit the game.")


def insuranceCheck(deck, dealersCards):
    print(f"Dealer's first card is: {deck[dealersCards[1]][0]}")
    if deck[dealersCards[1]][0] == "A" or deck[dealersCards[1]][0] == "J" or deck[dealersCards[1]][0] == "Q" or deck[dealersCards[1]][0] == "K" or deck[dealersCards[1]][0] == "10":
        if len(dealersCards) <= 3:
            return 1
    return 0


def insurance(bet):
    while True:
        output = input("Do you want insurance? (Y/N)\n>")
        if output.upper() == "Y" or output.upper() == "YES":
            insurance_cost = bet / 2
            return 1, insurance_cost
        elif output.upper() == "N" or output.upper() == "NO":
            return 0, insurance_cost
        else:
            print("You need to type 'Y' for Yes or 'N' for NO!")
    return -1



def gameLoop(deck, deckindex, bet, money):
    i = 1
    isInsurance = 0
    isInsuraceInusred = 0
    while True:
        print("DEALER: ???")
        if i == 1:
            deckindex = dealerCardsDysplay(deck, deckindex, True)
        else:
            deckindex = dealerCardsDysplay(deck, deckindex, False)
        print(f"PLAYER:")
        if i == 1:
            deckindex = addPlayerCard(deckindex)
            deckindex = addPlayerCard(deckindex)
        if deckindex >= len(deck) - 4:
            deck = deckShuffle()
            deckindex = 0
        PCS = CardsSum(deck, playersCards)
        displayCards(deck, playersCards)
        print(f"Your cards sum is: {PCS}")
        if PCS > 21:
            print("You busted! Dealer wins.")
            break
        elif PCS == 21:
            input("You have 21! Press Enter to continue...\n>")
            break
        dealersCardsSum = CardsSum(deck, dealersCards[1:len(dealersCards)])
        isInsurance = insuranceCheck(deck, dealersCards)
        if isInsurance == 1:
            if isInsuranceAsking == True:
                output, insurance_cost = insurance(bet)
                if output == 1:
                    isInsuraceInusred = 1
        if dealersCardsSum == 21:
            if isInsuraceInusred == 1:
                print("Dealer has 21! But you are insured so you dont lose your bet.")
                break 
            print("Dealer has 21!")
            break
        else:
            if isInsuraceInusred == 1:
                print("Dealer does not have 21!")
                money -= int(insurance_cost)
                print(f"You lost {int(insurance_cost)} coins for insurance. You have {money} coins left.")
        deckindex, playerchoiced, bet = playerChoice(deck, deckindex, bet)
        if playerchoiced == "end":
            break
        i += 1
    PCS = CardsSum(deck, playersCards)
    result = endGame(deck, deckindex, bet, PCS, dealersCards, isInsuraceInusred)
    return result, deck, deckindex, money

def CardsSum(deck, Cards):
        CardsSum = 0
        aceCount = 0
        for i in range(len(Cards)):
            if deck[Cards[i]][0] == "J" or deck[Cards[i]][0] == "Q" or deck[Cards[i]][0] == "K":
                CardsSum += 10
            elif deck[Cards[i]][0] == "A":
                aceCount += 1
            else:
                CardsSum += (int)(deck[Cards[i]][0])
            CardsSum += aceCount
        while aceCount > 0 and CardsSum + 10 <= 21:
            CardsSum += 10
            aceCount -= 1
        return CardsSum


def playerChoice(deck, deckindex, bet):
    while True:
        if len(playersCards) == 2:
            choice = input("Do you want to hit or stand or Double? (H/S/D)\n>")
        else: 
            choice = input("Do you want to hit or stand? (H/S)\n>")
        if choice.lower() == "h":
            deckindex = addPlayerCard(deckindex)
            return deckindex, "continue", bet
        elif choice.lower() == "s":
            return deckindex, "end", bet
        elif choice.lower() == "d" and len(playersCards) == 2:
            deckindex, bet = playerDouble(deckindex, bet)
            return deckindex, "end", bet
        else:
            print("Please enter 'H' to hit or 'S' to stand.")
            playerChoice( deck, deckindex, bet)


def playerDouble(deckindex, bet):
    bet = bet * 2
    print(f"Your bet is now {bet} coins.")
    deckindex = addPlayerCard(deckindex)
    return deckindex, bet


def addPlayerCard(deckindex):
    playersCards.append(deckindex)
    deckindex += 1
    return deckindex


def endGame(deck, deckindex, bet, PCS, dealersCards, insured):
    dealersCards.remove(len(deck) - 1)
    dealerSum = CardsSum(deck, dealersCards)
    if PCS > 21:
        return -bet
    while dealerSum <= 17:
        deckindex = dealerHit(deckindex)
        dealerSum = CardsSum(deck, dealersCards)
        if deckindex >= (len(deck) - 1):
            deck = deckShuffle()
            deckindex = 0

    print("DEALER:")
    displayCards(deck, dealersCards)
    print(f"Dealer's cards sum is: {dealerSum}")

    print("PLAYER: ")
    displayCards(deck, playersCards)
    print(f"Your cards sum is: {PCS}")

    input("Press Enter to see the result!\n>")

    result = gameResults(deck, bet, PCS, dealersCards, insured)

    return result


def gameResults(deck, bet, PCS, dealersCards, insured):
    dealerSum = CardsSum(deck, dealersCards)
    if PCS == 21 and len(playersCards) == 2:
        print("Blackjack! You win!")
        return int(bet * 1.5)
    elif PCS > 21:
        print("You busted! Dealer wins.")
        return -bet
    elif dealerSum > 21:
        print("Dealer busted! You win.")
        return bet
    elif dealerSum == 21 and len(dealersCards) == 2:
        if insured == 1:
            return 0
        print("Dealer has Blackjack! Dealer wins.")
        return -bet
    elif PCS > dealerSum:
        print("You win!")
        return bet
    elif PCS < dealerSum:
        print("Dealer wins!")
        return -bet
    else:
        print("It's a tie!")
        return 0


def dealerHit(deckindex):
    dealersCards.append(deckindex)
    deckindex += 1
    return deckindex


def dealerCardsDysplay(deck, index, first):
        if first:
            dealersCards.append(len(deck)-1)
            index = dealerHit(index)
            index = dealerHit(index)
        displayCards(deck, dealersCards[:(len(dealersCards)-1)])
        return index


def displayCards(deck, indexs):
    for i in range(len(indexs)):
        print(f" {_TOPBORDER} ",end=" ")
    print("\n",end="")
    for i in range(len(indexs)):
        print(f"|{deck[indexs[i]][1]}{_SPACING}|",end=" ")
    print("\n",end="")
    for i in range(len(indexs)):
        if deck[indexs[i]][0] == "10":
            print(f"|{deck[indexs[i]][0]} |",end=" ")
        else:
            print(f"| {deck[indexs[i]][0]} |",end=" ")
    print("\n",end="")
    for i in range(len(indexs)):
        print(f"|{_BOTTOMBORDER}{deck[indexs[i]][1]}|",end=" ")
    print("\n",end="")

    

def main(deckindex, deck):
    global money
    while money > 0:
        if deckindex >= (len(deck) - 4):
            deck = deckShuffle()
            print("\nDeck has been shuffled!\n ")
            deckindex = 0
        bet = gameStart(money)
        result, deck, deckindex, money = gameLoop(deck, deckindex, bet, money)
        money += result
        gamereset(deckindex, deck)


def gamereset(deckindex, deck):
    global money
    global isasking
    dealersCards.clear()
    playersCards.clear()
    if money <= 0:
        print("You have no more coins left. Game over!")
        input("Press Enter to exit the game!\n>")
        exit(0)
    print(f"You have {money} coins.")
    while True:
        if isasking == 1:
            output = input("Do you want to continue? (Y/N)\n>")
            if str(output).upper() == "Y":
                return
            elif str(output).upper() == "N":
                exit(0)
            else:
                print("You need to type 'Y' for Yes or 'N' for no.")
        else:
            input("Press Enter to continue to the next round!\n>")
            return

print(f"Hi fellow partner! Welcome to the wild frontier. Dust off your boots, tip your hat, and step right up to the bar. To get your winning streak started, we've loaded your saddlebag with {money} coins. Keep your eyes sharp, play your cards right, and let's see if you can make a fortune out here!")
main(deckindex, deck = deckShuffle())