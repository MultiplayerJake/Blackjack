import random

#Starter Values
money = 5000
suits = ('♥', '♦', '♠', '♣')
_singleDeck = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
deckindex = 0
game = True


#Decks:
deckValues = _singleDeck * 4
deckValues = list(deckValues)

deckSuits = (suit for suit in suits for _ in _singleDeck)
deckSuits = list(deckSuits)

dealersCards = []
playersCards = []

_spacing = " " * 2
_topBorder = "_" * 3
_bottomBorder = "_" * 2


def deckShuffle():
    deck = list(zip(deckValues, deckSuits))
    random.shuffle(deck)
    deck.append(("#", "#"))
    return deck


def gameStart(money):
    while True:
        print(f"Hi fellow partner! Welcome to the wild frontier. Dust off your boots, tip your hat, and step right up to the bar. To get your winning streak started, we've loaded your saddlebag with {money} coins. Keep your eyes sharp, play your cards right, and let's see if you can make a fortune out here!")
        print(f"\nYou have {money} coins")
        bet = input("How much do you bet? (1-5000, or QUIT)\n>")
        try:
            bet = int(bet)
            return bet
        except:
            bet = str(bet)
            if bet.upper() == "QUIT":
                exit(0)
            print("Error: Please enter a valid number or 'QUIT' to exit the game.")
        

def gameLoop(deck, deckindex, bet):
    i = 1
    while True:
        print("DEALER: ???")
        if i == 1:
            dealercardsDysplay(deck, deckindex, True, True)
            deckindex += 1
        else:
            dealercardsDysplay(deck, deckindex, False, False)
        print(f"PLAYER:")
        if i == 1:
            deckindex = addPlayerCard(deckindex)
            deckindex = addPlayerCard(deckindex)
        PCS = CardsSum(deck, playersCards)
        CardDyslpay(deck, playersCards)
        print(f"Your cards sum is: {PCS}")
        if PCS > 21:
            print("You busted! Dealer wins.")
            break
        deckindex, playerchoice = plyaerchosing(True, deck, deckindex, bet)
        if playerchoice == "end":
            break
        i += 1
    result = endGame(deck, deckindex, bet, PCS, dealersCards)
    return result

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

def plyaerchosing(first, deck, deckindex, bet):
    while True:
        if first:
            choice = input("Do you want to hit or stand or Double? (H/S/D)\n>")
        else: 
            choice = input("Do you want to hit or stand? (H/S)\n>")
        if choice.lower() == "h":
            deckindex = playerHit(deck, deckindex)
            print(deckindex)
            return deckindex, "continue"
        elif choice.lower() == "s":
            playerStand()
            return deckindex, "end"
        elif choice.lower() == "d" and first:
            print("You chose to hit.")
            deckindex = playerDouble(deck, deckindex, bet)
            return deckindex, "end"
        else:
            print("Please enter 'H' to hit or 'S' to stand.")
        first = False

def playerHit(deck, deckindex):
    deckindex = addPlayerCard(deckindex)
    return deckindex

def playerStand():
    print("You chose to stand.")
    return

def playerDouble(deck, deckindex, bet):
    print("You chose to double.")
    bet = bet * 2
    print(f"Your bet is now {bet} coins.")
    deckindex = playerHit(deck, deckindex)
    return deckindex

def addPlayerCard(deckindex):
    playersCards.append(deckindex)
    deckindex += 1
    return deckindex

def endGame(deck, deckindex, bet, PCS, dealersCards):
    dealersCards.remove(len(deck) - 1)
    dealersCardsSum = CardsSum(deck, dealersCards)
    while dealersCardsSum <= 17:
        deckindex = dealerHit(deck, deckindex)
        dealersCardsSum = CardsSum(deck, dealersCards)
    print("DEALER:")
    dealercardsDysplay(deck, deckindex, False, False)
    print(f"Dealer's cards sum is: {dealersCardsSum}")

    print("PLAYER: ")
    CardDyslpay(deck, playersCards)
    print(f"Your cards sum is: {PCS}")

    input("Press Enter to see the result!\n>")

    result = gameResults(deck, bet, PCS, dealersCards)

    return result

def gameResults(deck, bet, PCS, dealersCards):
    dealersCardsSum = CardsSum(deck, dealersCards)
    if PCS > 21:
        print("You busted! Dealer wins.")
        return -bet
    elif dealersCardsSum > 21:
        print("Dealer busted! You win.")
        return bet
    elif PCS > dealersCardsSum:
        print("You win!")
        return bet
    elif PCS < dealersCardsSum:
        print("Dealer wins!")
        return -bet
    else:
        print("It's a tie!")
        return 0

def dealerHit(deck, deckindex):
    dealersCards.append(deckindex)
    deckindex += 1
    return deckindex


def dealercardsDysplay(deck, index, add, first):
        if first:
            dealersCards.append(len(deck)-1)
        if add:
            dealersCards.append(index)
        CardDyslpay(deck, dealersCards)

def CardDyslpay(deck, indexs):
    for i in range(len(indexs)):
        print(f" {_topBorder} ",end=" ")
    print("\n",end="")
    for i in range(len(indexs)):
        print(f"|{deck[indexs[i]][1]}{_spacing}|",end=" ")
    print("\n",end="")
    for i in range(len(indexs)):
        if deck[indexs[i]][0] == "10":
            print(f"|{deck[indexs[i]][0]} |",end=" ")
        else:
            print(f"| {deck[indexs[i]][0]} |",end=" ")
    print("\n",end="")
    for i in range(len(indexs)):
        print(f"|{_bottomBorder}{deck[indexs[i]][1]}|",end=" ")
    print("\n",end="")

    

def main(deckindex, money):
    deck = deckShuffle()
    bet = gameStart(money)
    result = gameLoop(deck, deckindex, bet)
    money += result
    gamereset(deckindex, money)

def gamereset(deckindex, money):
    dealersCards.clear()
    playersCards.clear()
    print(f"You have {money} coins.")
    while True:
        output = input("Do you want to continue? (Y/N)\n>")
        print(output.upper())
        if str(output).upper() == "Y":
            print(money)
            main(deckindex, money)
        elif str(output).upper() == "N":
            exit(0)
        else:
            print("You need to type 'Y' for Yes or 'N' for no.")
        

main(deckindex, money)