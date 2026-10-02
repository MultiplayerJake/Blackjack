import random

#Starter Values
money = 5000
_SUITS = ('♥', '♦', '♠', '♣')
_SINGLEDECK = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
deckindex = 0
game = True


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


def deckShuffle():
    deck = list(zip(deckValues, deckSuits))
    random.shuffle(deck)
    deck.append(("#", "#"))
    print("\nDeck has been shuffled!\n ")
    return deck


def gameStart(money):
    while True:
        print(f"\nYou have {money} coins")
        bet = input(f"How much do you bet? (1-{money}, or QUIT)\n>")
        try:
            bet = int(bet)
            if bet >= 1 and bet <= money:
                return bet
            else:
                print(f"Please enter a number between 1 and {money}.")
        except:
            if bet.upper() == "QUIT":
                exit(0)
            print("Error: Please enter a valid number or 'QUIT' to exit the game.")
        

def gameLoop(deck, deckindex, bet):
    i = 1
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
        dealersCardsSum = CardsSum(deck, dealersCards[1:len(dealersCards)-1])
        if dealersCardsSum == 21:
            print("Dealer has 21!")
            break
        deckindex, playerchoice, bet = playerChoice(True, deck, deckindex, bet)
        if playerchoice == "end":
            break
        i += 1
    PCS = CardsSum(deck, playersCards)
    result = endGame(deck, deckindex, bet, PCS, dealersCards)
    return result, deck, deckindex


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
        # Handle aces after calculating other card values
        for i in range(aceCount):
            if CardsSum + 11 > 21:
                CardsSum += 1
            else:
                CardsSum += 11
        return CardsSum


def playerChoice(first, deck, deckindex, bet):
    while True:
        if first:
            choice = input("Do you want to hit or stand or Double? (H/S/D)\n>")
        else: 
            choice = input("Do you want to hit or stand? (H/S)\n>")
        if choice.lower() == "h":
            deckindex = addPlayerCard(deckindex)
            return deckindex, "continue", bet
        elif choice.lower() == "s":
            return deckindex, "end", bet
        elif choice.lower() == "d" and first:
            deckindex, bet = playerDouble(deckindex, bet)
            return deckindex, "end", bet
        else:
            print("Please enter 'H' to hit or 'S' to stand.")
            playerChoice(first, deck, deckindex, bet)
        first = False


def playerDouble(deckindex, bet):
    bet = bet * 2
    print(f"Your bet is now {bet} coins.")
    deckindex = addPlayerCard(deckindex)
    return deckindex, bet


def addPlayerCard(deckindex):
    playersCards.append(deckindex)
    deckindex += 1
    return deckindex


def endGame(deck, deckindex, bet, PCS, dealersCards):
    dealersCards.remove(len(deck) - 1)
    dealerSum = CardsSum(deck, dealersCards)
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

    result = gameResults(deck, bet, PCS, dealersCards)

    return result


def gameResults(deck, bet, PCS, dealersCards):
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

    

def main(deckindex, money, deck):
    if deckindex >= (len(deck) - 4):
        deck = deckShuffle()
        deckindex = 0
    bet = gameStart(money)
    result, deck, deckindex = gameLoop(deck, deckindex, bet)
    money += result
    gamereset(deckindex, money, deck)


def gamereset(deckindex, money, deck):
    dealersCards.clear()
    playersCards.clear()
    if money <= 0:
        print("You have no more coins left. Game over!")
        input("Press Enter to exit the game!\n>")
        exit(0)
    print(f"You have {money} coins.")
    while True:
        output = input("Do you want to continue? (Y/N)\n>")
        if str(output).upper() == "Y":
            main(deckindex, money, deck)
        elif str(output).upper() == "N":
            exit(0)
        else:
            print("You need to type 'Y' for Yes or 'N' for no.")   

print(f"Hi fellow partner! Welcome to the wild frontier. Dust off your boots, tip your hat, and step right up to the bar. To get your winning streak started, we've loaded your saddlebag with {money} coins. Keep your eyes sharp, play your cards right, and let's see if you can make a fortune out here!")
main(deckindex, money, deck = deckShuffle())
