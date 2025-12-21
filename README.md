# BlackJack-98

A Windows 98 inspired game of Blackjack! Made with Tkinter. Theme and design inspired by the game Solitaire found in [98.js - Windows 98 Online](https://98.js.org/)

![A screenshot  of the game](/resources/images/display.png)

## The rules are simple

1. Four cards are drawn at the start of the game, two each for the player and the dealer with one of the dealers cards being face down.
2. The player may draw a card ("hit") to increase its odds of winning by getting as close to 21 as possible.
3. If the player total of cards exceed 21 while drawing, the player loses (busts).
4. Once the player is satisfied with their current hand, press the "stay" button, now it's the dealers turn.
5. The dealer reveals the facedown card, if the total in the dealers current hand is below 17, the dealer draws a card.
6. If the dealers total exceeds 21 while drawing, the player wins.
7. Once dealer has drawn enough cards to reach 17 or higher, the totals of both hands are compared.
8. The highest hand wins while the other loses, if both hands have the same total values it ends in a tie.

## Controls

Two buttons, one for "Hit" and one for "Stand".
The menu has a new game option, it is also tied to the "F2" key on the keyboard for a quick and easy new game.

## Try it out yourself!

1.  Clone it to your local repository, once done, navigate to directory:
```
git clone https://github.com/ME-Alchemist/BlackJack-98.git

cd BlackJack-98
```
---

2. Create a virtual environment:
```
py -m venv .venv
```
---

4. Press `Ctrl + Shift + P`, choose `Python Select Interperter` and select your newly created virtual environment
---

5. Install the required packages in requirements.txt
```
pip install -r requirements.txt
```
---

6.  Run it through the terminal
```
python ./blackjack_gui.py
```

## Things left to do

- Add menubar **`Done!`**
- Use spritesheet for displaying cards **`Done!`**
- Randomize face down card **`Done!`**
- Add sound effects **`Done!`**
- Add appropriate sound library for sound control
- Add game reset functionality **`Done!`**
- Event tracking (whose turn is it/Progress) **`Done!`**
- Add Win/lose counter **`Done!`**
- Add tooltips
- Additional logic for dealer and player **`Done!`**
- Clean up code  **`Almost done`**
