from PIL import Image, ImageTk
import random as rand

card1ls = [
           {'Suit': '♥', 'value': 8, 'l': 0, 't': 0, 'r': 71, 'b': 96},
           {'Suit': '♥', 'value': 8, 'l': 355, 't': 192, 'r': 426, 'b': 288}
           ]

random_int = rand.randint(1, 12)
random_left = 71 * random_int
face_down_cards = {'Suit': '♥', 'value': 8, 'l': random_left, 't': 384, 'r': random_left + 71, 'b': 480}

def load_card_images(hand):
    #  load up spritesheet
    photo_images = []
    for card in hand:
        left = card["l"]
        top = card["t"]
        right = card["r"]
        bottom = card["b"]

        img_path = "resources/images/spritesheet.png"
        img = Image.open(img_path)
        img = img.crop((left, top, right, bottom))
        img = ImageTk.PhotoImage(img)

        # return a list of tkinter PhotoImage objects
        photo_images.append(img)
        
    return photo_images


def load_single_card_image(card):
    left = card["l"]
    top = card["t"]
    right = card["r"]
    bottom = card["b"]

#  load up spritesheet
    img_path = "resources/images/spritesheet.png"
    img = Image.open(img_path)
    img = img.crop((left, top, right, bottom))
    photo_img = ImageTk.PhotoImage(img)
    
    return photo_img


# Create a Card class to represent each card in the deck
# left, top, right, bottom to crop out a single card with PIL
class Card:
    def __init__(self, suit, value, l, t, r, b):
        self.suit = suit
        self.value = value
        self.l = l
        self.t = t
        self.r = r
        self.b = b
    
    def __str__(self):
        return f"{self.value} of {self.suit})"
    
    def to_dict(self):
        return {"Suit": self.suit, "value": self.value, "l": self.l, "t": self.t, "r": self.r, "b": self.b }
    


def shuffleCards(list_of_cards):
    # look up fisher yates as alternative for extra challenge
    import random as rd
    rd.shuffle(list_of_cards)
    return list_of_cards 
    

'''
create a list of dictionaries for each card
use "left", "top", "right", "bottom" to crop out card
from loaded image (spritesheet), instead of manually
saving 52 individual images
'''
def generate_game():
    # Generate the cards
    suits =["\u2663", "\u2666","\u2665","\u2660"]
    values = ["A",2,3,4,5,6,7,8,9,10,"J","Q","K"]
    cards = []

    l = 0
    t = 0
    r = 71
    b = 96

    for suit in suits:
        for value in values:
            card = Card(suit, value, l, t, r, b)
            cards.append(card.to_dict())
            l += 71
            r += 71
        l = 0
        r = 71
        b += 96
        t += 96
                    
    # shuffle the cards
    return shuffleCards(cards)


def player_cards(deck):
    # deal two cards to player and dealer
    player_hand = []
    for i in range (2):
        player_hand.append(takeACard(deck))
    return player_hand


def dealer_cards(deck):
    # deal two cards to dealer
    dealer_hand = []
    for i in range(2):
        dealer_hand.append(takeACard(deck))
    return dealer_hand


# pick a card from the shuffled deck
def takeACard(listofcards):
    drawn_card = listofcards.pop()
    return drawn_card

'''
once the player "stays", the dealer
reveals the face down card and counts
the total in its hand
''' 

# count the total in either the player or the dealer's hand
def count_total(hand):
    total = 0
    ace_count = 0

    for card in hand:

        match card["value"]:
            case "J" | "Q" | "K":
                total += 10
            case "A":
                total += 11
                ace_count += 1
            case _:
                total += card["value"]

    while total > 21 and ace_count >= 1:
        total -= 10
        ace_count -= 1
                        
    return total


# For testing code
if __name__ == "__main__":
    pass