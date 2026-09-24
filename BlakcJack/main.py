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
            return
        except:
            ...

def gameLoop(deck, deckindex):
    i = 1
    while game:
        print("DEALER: ???")
        if i == 1:
            dealercardsDysplay(deck, deckindex, True)
        else:
            dealercardsDysplay(deck, deckindex, False)
        deckindex += 1
        return


def dealercardsDysplay(deck, index, add):
        print(deckValues)
        dealersCards.append(len(deck)-1)
        if add == False:
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
    gameStart()
    gameLoop(deck, deckindex)

main(deckindex)