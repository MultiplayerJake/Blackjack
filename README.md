# Blackjack

A simple terminal Blackjack game written in Python. You start with **5000 coins**, bet on every round and try to beat the dealer without going over 21.

Play it from the source:

or just run the pre-built Windows executable

## Python version

The game is written for **Python 3.6 or newer** (it uses `f-strings` and `random.shuffle`).

It is developed and tested on **Python 3.11 / 3.12** on Windows, but there is nothing Windows-specific in the code, so it runs on Linux and macOS too.

No third-party packages are needed to *play* the game.


## Features

* **Betting** — choose your bet each round (1 up to all the coins you own).
* **Hit / Stand** — classic player choices, with your hand total shown after every move.
* **Double** — double your bet on the first two cards and receive one more card.
* **Insurance** — when the dealer's upcard is a 10-value card or an Ace you can buy insurance for half of your bet; can be enabled/disabled in settings.
* **Blackjack payout** — a natural 21 pays **3:2**.
* **Settings menu** — reachable while placing a bet (type `setting`):
  * `Asking` (`a`, `ask`, `asking`) — turn the "Do you want to continue?" question on/off between rounds.
  * `Insurance` (`I`, `insurance`) — turn the insurance question on/off.
* **Quit anytime** — type `quit` while betting to exit.
* **Auto-shuffle** — the deck (4 × 52 cards) is reshuffled automatically when it runs low.
* **ASCII card display** — cards are printed as small ASCII boxes with suits `♥ ♦ ♠ ♣`.
* **Bankroll tracking** — you lose the game when your coins drop to 0.

---

## How does this project work?

### Program flow

```
main()
 └─ loop while money > 0
     ├─ reshuffle the deck if it is almost empty
     ├─ gameStart()        → ask for a bet (or quit / open settings)
     ├─ gameLoop()         → play one round
     │    ├─ deal 2 player cards + 2 dealer cards (one hidden)
     │    ├─ gameLoopChecking() → bust/blackjack/insurance checks
     │    ├─ playerChoice() → hit / stand / double
     │    └─ endGame()     → dealer draws to 17, compare hands
     │         └─ gameResults() → returns +bet, -bet, 0 or +1.5·bet
     ├─ money += result
     └─ gamereset()        → clear both hands, ask to continue
```

### Key ideas

1. **The deck** — two parallel lists are zipped together in `deckShuffle()`:
   * `deckValues` = `['2'...'A'] * 4`
   * `deckSuits` = every suit repeated 13 times  

   The result is a list of `(value, suit)` tuples, plus a `("#", "#")` sentinel card that is appended at the end and used as the dealer's face-down card.

2. **Cards as indexes** — `playersCards` and `dealerCards` don't store cards, they store *positions in the deck*. `addPlayerCard()` / `dealerHit()` simply append the current `deckindex` and move it forward. The cards are only looked up when they are displayed or summed.

3. **Scoring** — `CardsSum()` adds 10 for `J/Q/K`, 1 for `A` at first, and then promotes Aces to 11 one by one as long as the total stays ≤ 21.

4. **Dealer AI** — in `endGame()` the dealer reveals its hidden card and keeps hitting while its sum is `<= 17`.

5. **Result** — `gameResults()` compares the two totals and returns a signed number (profit/loss), which `main()` adds to `money`.

6. **State** — most of the game state (`money`, `playersCards`, `dealerCards`, the settings flags) lives in global variables, and functions mutate them directly.

---

## Known issues
* **Mid-round reshuffle loses the cards.** If the deck runs out *during* a round, `gameLoop()`/`endGame()` shuffle a local copy of the deck while the old card indexes are kept, so the wrong cards (or an `IndexError`) can show up. The reshuffle in `endGame()` is never returned to the caller at all.

---

## What I want to add to the game

* **Split** — split a matching pair into two separate hands (and play each of them for its own bet).
* **Bank** — borrow more coins than you currently own and pay the debt back when you win.
* **Loading settings from a JSON file** — so `settings.json` keeps your insurance/asking preferences between runs, instead of resetting every launch.
* **Make dealer reveal cards one by one** — add a option to reveal cards one by one.
I would add this too settings so you can turn it on/off. 

### Made as an student projekt at **ITG** with [charalizee](https://github.com/charalizee) as a tester. Inspired by [Inventwithpython.](https://inventwithpython.com/bigbookpython/project4.html#)
