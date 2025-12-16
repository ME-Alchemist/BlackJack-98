import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import tkinter.ttk as ttk
import blackjack as game
import winsound as sfx
import os

deck = game.generate_game()
player = game.player_cards(deck)
dealer = game.dealer_cards(deck)
background = "#008000"

wins = 0
lose = 0
Tie = 0


def reset():
    global deck, player, dealer, photo_dealer, photo_player, face_down_card
    deck.clear()
    player.clear()
    dealer.clear()
    photo_player.clear()
    photo_dealer.clear()
    destroy_dealer()
    destroy_player()
    deck = game.generate_game()
    player = game.player_cards(deck)
    dealer = game.dealer_cards(deck)
    photo_player = game.load_card_images(player)
    photo_dealer = game.load_card_images(dealer)
    face_down_card = game.load_single_card_image(game.face_down_cards)
    player_play()
    dealer_play()
    dealerInt.set(game.count_total(dealer[1:]))
    playerInt.set(game.count_total(player))
    event_label.configure(text="It's the players turn. Hit or stay?", foreground="black")
    hit_btn.configure(state="active")
    stay_btn.configure(state="active")

    # if os.name == 'nt':
    #     _ = os.system('cls') # for Windows
    # else:
    #     _ = os.system('clear') # for Linux/macOS

    print(f"Player's hand: {player}")
    print(f"Dealer's hand: {dealer}")


play_lose = lambda: sfx.PlaySound("resources/sounds/CHORD.wav", sfx.SND_ASYNC)
play_win = lambda: sfx.PlaySound("resources/sounds/TADA.wav", sfx.SND_ASYNC)
play_tie = lambda: sfx.PlaySound("resources/sounds/CHIMES.WAV", sfx.SND_ASYNC)


def check_player():
    event_label.configure(text="Player chose to hit")
    card = game.takeACard(deck)
    card_img = game.load_single_card_image(card)
    player.append(card)
    photo_player.append(card_img)
    pack_card_img = tk.Label(player_card_frame, image=card_img, bg=background)
    pack_card_img.pack(side="left")  
    print(f"Player's hand: {player}")
    playerInt.set(game.count_total(player))

    if game.count_total(player) < 21:
        return
    elif game.count_total(player) > 21:
        event_label.configure(text="Player busts! you lose.", foreground="red")

        hit_btn.configure(state="disabled")
        stay_btn.configure(state="disabled")
        play_lose()


# after the player is done taking cards and chooses to "stay"
# check the dealer's hand, here we reveal the face down card and draw a card if it's total is less than 17
def player_stays():
    event_label.configure(text="Player stands")
    dealer_card_facedown.configure(image=photo_dealer[0])
    dealerInt.set(game.count_total(dealer))
    hit_btn.configure(state="disabled")
    stay_btn.configure(state="disabled")

    while game.count_total(dealer) < 17:
        event_label.configure(text="Dealer must draw (total < 17)")
        card = game.takeACard(deck)
        card_img = game.load_single_card_image(card)
        dealer.append(card)
        photo_dealer.append(card_img)
        pack_card_img = tk.Label(dealer_card_frame, image=card_img, bg=background)
        pack_card_img.pack(side="left") 
        dealerInt.set(game.count_total(dealer))

    if game.count_total(dealer) > 21:
        event_label.configure(text="Dealer busts! (total > 21) you win!")
        play_win()

    elif game.count_total(dealer) <= 21 and game.count_total(dealer) > game.count_total(player):
        event_label.configure(text="The dealer wins! (dealer total > player total)")
        play_lose()

    elif game.count_total(dealer) == game.count_total(player):
        event_label.configure(text="It's a tie! (dealer total == player total)")
        play_tie()

    elif game.count_total(dealer) < game.count_total(player):
        event_label.configure(text="You win! (dealer total < player total)")
        play_win()

print(f"Player's hand: {player}")
print(f"Dealer's hand: {dealer}")

# main window with title and size
main_window = tk.Tk()
main_window.option_add('*tearOff', False)
main_window.title(string="Blackjack Windows 98 Edition")
main_window.geometry("800x480")
main_window.config(bg=background)
main_window.resizable(width=None, height=None)

theme = ttk.Style(master=main_window)
print(theme.theme_names())
theme.theme_use("vista")

# A menu for the main window, to reset the game or exit
menubar = tk.Menu(main_window)
main_window['menu'] = menubar
menu_file = tk.Menu(menubar)
menu_file.add_command(label="New Game...", underline=1, command= lambda: [reset()])
menubar.add_cascade(label="Game", menu=menu_file)
main_window.config(menu=menubar)


# load card images
photo_player = game.load_card_images(player)
photo_dealer = game.load_card_images(dealer)
face_down_card = game.load_single_card_image(game.face_down_cards)


# Create frames, windows
dealer_frame = tk.LabelFrame(main_window, 
                             width=630, 
                             height=160, 
                             relief="sunken", 
                             borderwidth=2, 
                             bg=background, 
                             text="Dealer", 
                             font=("MS Sans Serif", 10, "bold"))
dealer_frame.pack_propagate(0)
dealer_frame.pack(pady=30)

dealer_card_frame = tk.Frame(dealer_frame, width=480, height=100, bg=background)
dealer_card_frame.pack()

# Keep track of the last action taken
event_frame = tk.Frame(main_window, bg=background,)
# event_text = tk.Text(event_frame, "It's the players turn. Hit or stay?")
event_label = tk.Label(event_frame, text="It's the players turn. Hit or stay?", bg=background, font=("MS Sans Serif", 10, "bold"))
event_frame.pack()
event_label.pack()


player_frame = tk.LabelFrame(main_window, 
                             width=630, 
                             height=160, 
                             relief="sunken", 
                             borderwidth=2, 
                             bg=background, 
                             text="Player", 
                             font=("MS Sans Serif", 10, "bold"))
player_frame.pack_propagate(0)
player_frame.pack(pady=20)

dealer_total_frame = tk.Frame(dealer_frame, width=200, height=50, bg=background)
dealer_total_frame.pack()
dealerInt = tk.IntVar(dealer_total_frame, game.count_total(dealer[1:]))
dealer_label = tk.Label(dealer_total_frame, text="Total:", font=("MS Sans Serif", 10, "bold"), bg=background)
dealer_label.pack(side="left")
dealer_total = tk.Label(dealer_total_frame, textvariable=dealerInt, bg=background, font=("MS Sans Serif", 10, "bold"))
dealer_total.pack()


player_total_frame = tk.Frame(player_frame, width=200, height=50, bg=background)
player_total_frame.pack()
playerInt = tk.IntVar(player_total_frame, game.count_total(player))
player_label = tk.Label(player_total_frame, text="Total:",  font=("MS Sans Serif", 10, "bold"), bg=background)
player_label.pack(side="left")
player_total = tk.Label(player_total_frame, textvariable=playerInt, bg=background, font=("MS Sans Serif", 10, "bold"))
player_total.pack()

player_card_frame = tk.Frame(player_frame, width=480, height=100, bg=background)
player_card_frame.pack()


def player_play():
    global player_card_1, player_card_2
    player_card_1 = tk.Label(player_card_frame, image=photo_player[0], bg=background)
    player_card_1.pack(side="left")
    player_card_2 = tk.Label(player_card_frame, image=photo_player[1], bg=background)
    player_card_2.pack(side="left")

player_play()

def destroy_player():
    for label in player_card_frame.winfo_children():
        label.destroy()
    player_card_1.destroy()
    player_card_2.destroy()



def dealer_play():
    global dealer_card_facedown, dealer_card_faceup
    dealer_card_facedown = tk.Label(dealer_card_frame, image=photo_dealer[0], bg=background)
    dealer_card_facedown.configure(image=face_down_card)
    dealer_card_facedown.pack(side="left", pady=5)
    dealer_card_faceup = tk.Label(dealer_card_frame, image=photo_dealer[1], bg=background)
    dealer_card_faceup.pack(side="left")

dealer_play()

def destroy_dealer():
    for label in dealer_card_frame.winfo_children():
        label.destroy()
    dealer_card_facedown.destroy()
    dealer_card_faceup.destroy()



btn_frame = tk.Frame(main_window, width=200, height=50, bg=background)
btn_frame.pack()
hit_btn = tk.Button(btn_frame, text="Hit me!", relief="raised", command=check_player)
hit_btn.pack(side="left", padx=10)
stay_btn = tk.Button(btn_frame, text="Stay", relief="raised", command=player_stays)
stay_btn.pack()

main_window.mainloop()