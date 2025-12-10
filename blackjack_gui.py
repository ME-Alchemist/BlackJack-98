import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, PhotoImage
import tkinter.ttk as ttk
import blackjack as game
import winsound as sfx
import os

deck = game.generate_game()
player = game.player_cards(deck)
dealer = game.dealer_cards(deck)
background = "#008000"

def reset():
    global deck, player, dealer
    deck.clear()
    player.clear()
    dealer.clear()
    deck = game.generate_game()
    player = game.player_cards(deck)
    dealer = game.dealer_cards(deck)
    dealerInt.set(game.count_total(dealer))
    playerInt.set(game.count_total(player))
    hit_btn.configure(state="active")
    stay_btn.configure(state="active")


    if os.name == 'nt':
        _ = os.system('cls') # for Windows
    else:
        _ = os.system('clear') # for Linux/macOS

    print(f"Player's hand: {player}")
    print(f"Dealer's hand: {dealer}")


play_lose = lambda: sfx.PlaySound("resources/sounds/CHORD.wav", sfx.SND_ASYNC)
play_win = lambda: sfx.PlaySound("resources/sounds/TADA.wav", sfx.SND_ASYNC)

def check_player():
    if game.count_total(player) < 21:
        return
    elif game.count_total(player) > 21:
        # messagebox.showwarning("You lose!", "you lose!")
        hit_btn.configure(state="disabled")
        stay_btn.configure(state="disabled")
        play_lose()

    # elif game.count_total(player) > game.count_total(dealer) and game.count_total(player) <= 21:
    #     messagebox.showwarning("you win!", "you win!")

# after the player is done taking cards and chooses to "stay"
# check the dealer's hand, here we reveal the face down card and draw a card if it's total is less than 17

def player_stays():
    while game.count_total(dealer) < 17:
        dealer.append(game.takeACard(deck))
        print("Dealer takes another card")
    dealerInt.set(game.count_total(dealer))
    if game.count_total(dealer) > 21:
        messagebox.showinfo("Dealer busts!", "Dealer busts! You win!")
        play_win()
    elif game.count_total(dealer) >= game.count_total(player):
        messagebox.showinfo("You lose!", "Dealer wins!")
        play_lose()


list_of_lambda_commands = [
    lambda: player.append(game.takeACard(deck)), 
    lambda: print(f"Player's hand: {player}"), 
    lambda: playerInt.set(game.count_total(player)),
    lambda: check_player()
    ]

def run_all():
    for func in list_of_lambda_commands:
        func()

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
photo_player = game.load_card_image(player)
photo_dealer = game.load_card_image(dealer)


dealer_frame = tk.LabelFrame(main_window, 
                             width=630, 
                             height=160, 
                             relief="sunken", 
                             borderwidth=2, 
                             bg=background, 
                             text="Dealer", 
                             font=("Terminal", 15, "bold"))
dealer_frame.pack_propagate(0)
dealer_frame.pack(pady=30)

dealer_card_frame = tk.Frame(dealer_frame, width=480, height=100, bg=background)
dealer_card_frame.pack()

player_frame = tk.LabelFrame(main_window, 
                             width=630, 
                             height=160, 
                             relief="sunken", 
                             borderwidth=2, 
                             bg=background, 
                             text="Player", 
                             font=("Terminal", 15, "bold"))
player_frame.pack_propagate(0)
player_frame.pack(pady=20)

dealer_total_frame = tk.Frame(dealer_frame, width=200, height=50, bg=background)
dealer_total_frame.pack()
dealerInt = tk.IntVar(dealer_total_frame, game.count_total(dealer))
dealer_label = tk.Label(dealer_total_frame, text="Total:", font=("Terminal", 15, "bold"), bg=background)
dealer_label.pack(side="left")
dealer_total = tk.Label(dealer_total_frame, textvariable=dealerInt, bg=background, font=("Terminal", 15, "bold"))
dealer_total.pack()

event_frame = tk.Frame(main_window, bg=background)
event_text = tk.StringVar(event_frame, "The current text")
event_label = tk.Label(event_frame, textvariable=event_text, bg=background)
event_frame.pack()

player_total_frame = tk.Frame(player_frame, width=200, height=50, bg=background)
player_total_frame.pack()
playerInt = tk.IntVar(player_total_frame, game.count_total(player))
player_label = tk.Label(player_total_frame, text="Total:",  font=("Terminal", 15, "bold"), bg=background)
player_label.pack(side="left")
player_total = tk.Label(player_total_frame, textvariable=playerInt, bg=background, font=("Terminal", 15, "bold"))
player_total.pack()

player_card_frame = tk.Frame(player_frame, width=480, height=100, bg=background)
player_card_frame.pack()

for img in photo_player:
    player_card_img = tk.Label(player_card_frame, image=img, bg=background)
    player_card_img.pack(side="left")

for img in photo_dealer:
    dealer_card_img = tk.Label(dealer_card_frame, image=img, bg=background)
    dealer_card_img.pack(side="left", pady=5)


btn_frame = tk.Frame(main_window, width=200, height=50, bg=background)
btn_frame.pack()
hit_btn = tk.Button(btn_frame, text="Hit me!", relief="raised", command=lambda: run_all())
hit_btn.pack(side="left", padx=10)
stay_btn = tk.Button(btn_frame, text="Stay", relief="raised", command=lambda: messagebox.showinfo("Stay", "You chose to stay"))
stay_btn.pack()

main_window.mainloop()