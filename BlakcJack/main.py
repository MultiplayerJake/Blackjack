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

_welcome_text = "Hi fellow partner! Welcome to the wild frontier. Dust off your boots, tip your hat, and step right up to the bar. To get your winning streak started, we've loaded your saddlebag with 5000 coins. Keep your eyes sharp, play your cards right, and let's see if you can make a fortune out here!"
_spacing = " " * 2
_topBorder = "_" * 3
_bottomBorder = "_" * 2


def deckShuffle():
    deck = list(zip(deckValues, deckSuits))
    random.shuffle(deck)
    deck.append(("#", "#"))
    return deck


def gameStart():
    while True:
        print(_welcome_text)
        print(f"\nYou have {money} coins")
        bet = input("How much do you bet? (1-5000, or QUIT)\n>")
        try:
            bet = int(bet)
            return bet
        except:
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
        print("PLAYER: ")
        if i == 1:
            deckindex = addPlayerCard(deckindex)
            deckindex = addPlayerCard(deckindex)
        CardDyslpay(deck, playersCards)
        playerchse = plyaerchosing(True, deck, deckindex, bet)
        if playerchse == "end":
            break
        i += 1
    endGame()

def plyaerchosing(first, deck, deckindex, bet):
    while True:
        if first:
            choice = input("Do you want to hit or stand or Double? (H/S/D)\n>")
        else: 
            choice = input("Do you want to hit or stand? (H/S)\n>")
        if choice.lower() == "h":
            playerHit(deck, deckindex)
            break
        elif choice.lower() == "s":
            playerStand()
            return "end"
        elif choice.lower() == "d" and first:
            print("You chose to hit.")
            playerDouble(deck, deckindex, bet)
            break
        else:
            print("Please enter 'H' to hit or 'S' to stand.")
        first = False

def playerHit(deck, deckindex):
    deckindex = addPlayerCard(deckindex)
    CardDyslpay(deck, playersCards)
    return

def playerStand():
    print("You chose to stand.")
    return

def playerDouble(deck, deckindex, bet):
    print("You chose to double.")
    bet = bet * 2
    print(f"Your bet is now {bet} coins.")
    playerHit(deck, deckindex)
    return

def addPlayerCard(deckindex):
    playersCards.append(deckindex)
    deckindex += 1
    return deckindex

def endGame():
    print("Game Over. Thanks for playing!")
    return

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

    

def main(deckindex):
    deck = deckShuffle()
    bet = gameStart()
    gameLoop(deck, deckindex, bet)

main(deckindex)