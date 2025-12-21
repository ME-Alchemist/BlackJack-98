import tkinter as tk
import blackjack as game
import winsound as sfx
# import os

deck = game.generate_game()
player = game.player_cards(deck)
dealer = game.dealer_cards(deck)
background = "#008000"

# main window with title and size
main_window = tk.Tk()
main_window.option_add('*tearOff', False)
main_window.title(string="Blackjack Windows 98 Edition")
main_window.geometry("800x520")
main_window.config(bg=background)
main_window.resizable(width=None, height=None)

# A menu for the main window, to reset the game or exit
menubar = tk.Menu(main_window)
main_window['menu'] = menubar
menu_file = tk.Menu(menubar)
menu_file.add_command(label="New Game...", underline=1, accelerator="F2", command= lambda: [reset()])
menubar.add_cascade(label="Game", menu=menu_file)
main_window.config(menu=menubar)


def reset(event=None):
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

    # meant for clearing the terminal when starting a new game
    # not needed since print statements have been removed, but kept for reference
    # if os.name == 'nt':
    #     _ = os.system('cls') # for Windows
    # else:
    #     _ = os.system('clear') # for Linux/macOS

main_window.bind_all("<F2>", reset)


# sound effects
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
    playerInt.set(game.count_total(player))

    if game.count_total(player) < 21:
        return
    elif game.count_total(player) > 21:
        event_label.configure(text="Player busts! you lose.", foreground="red")
        lose.set(lose.get() +1)

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
        event_label.configure(text="Dealer busts! (total > 21) you win!", foreground="cyan")
        wins.set(wins.get() +1)
        play_win()

    elif game.count_total(dealer) <= 21 and game.count_total(dealer) > game.count_total(player):
        event_label.configure(text="The dealer wins! (dealer total > player total)", foreground="red")
        lose.set(lose.get() +1)
        play_lose()

    elif game.count_total(dealer) == game.count_total(player):
        event_label.configure(text="It's a tie! (dealer total == player total)", foreground="yellow")
        ties.set(ties.get() +1)
        play_tie()

    elif game.count_total(dealer) < game.count_total(player):
        event_label.configure(text="You win! (dealer total < player total)", foreground="cyan")
        wins.set(wins.get() +1)
        play_win()


# load card images
photo_player = game.load_card_images(player)
photo_dealer = game.load_card_images(dealer)
face_down_card = game.load_single_card_image(game.face_down_cards)
hit_img, stand_img = game.load_assets()


# Create frames, windows
dealer_frame = tk.LabelFrame(main_window, 
                             width=630, 
                             height=160, 
                            #  relief="sunken", 
                             borderwidth=2, 
                             bg=background, 
                             text="Dealer", 
                             font=("MS Sans Serif", 10, "bold"))
dealer_frame.pack_propagate(0)
dealer_frame.pack(pady=30)

dealer_card_frame = tk.Frame(dealer_frame, width=480, height=100, bg=background)
dealer_card_frame.pack()

# Keep track of the last action taken
event_frame = tk.Frame(main_window, bg=background)
event_label = tk.Label(event_frame, text="It's the players turn. Hit or stay?", bg=background, font=("MS Sans Serif", 10, "bold"))
event_frame.pack()
event_label.pack()

# Keep track of score
score_frame = tk.Frame(main_window,bg=background, height=20, width=100 )
score_frame.pack()

wins = tk.IntVar(score_frame, 0)
lose = tk.IntVar(score_frame, 0)
ties = tk.IntVar(score_frame, 0)

win_label = tk.Label(score_frame, text="Wins:", bg=background, font=("MS Sans Serif", 11, "bold"), foreground="cyan").pack(side="left")
score_wins = tk.Label(score_frame, textvariable=wins, bg=background, font=("MS Sans Serif", 11, "bold"), foreground="cyan").pack(side="left")
lose_label = tk.Label(score_frame, text="Loses:", bg=background, font=("MS Sans Serif", 11, "bold"), foreground="red").pack(side="left")
score_lose = tk.Label(score_frame, textvariable=lose, bg=background, font=("MS Sans Serif", 11, "bold"), foreground="red").pack(side="left")
tie_label = tk.Label(score_frame, text="Ties:", bg=background, font=("MS Sans Serif", 11, "bold"), foreground="yellow").pack(side="left")
score_ties = tk.Label(score_frame, textvariable=ties, bg=background, font=("MS Sans Serif", 11, "bold"), foreground="yellow").pack(side="left")

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


btn_frame = tk.Frame(main_window, width=200, height=5, bg=background)
btn_frame.pack()
# hit_label = tk.Label(btn_frame, image=hit_img, bg=background).pack(side="left", padx=5)
hit_btn = tk.Button(btn_frame, text="   Hit me!", image=hit_img, compound="left", relief="raised", command=check_player)
hit_btn.pack(side="left", padx=5)
# stand_label = tk.Label(btn_frame, image=stand_img, bg=background).pack(side="left", padx=5)
stay_btn = tk.Button(btn_frame, text="   Stand", image=stand_img, compound="left", relief="raised", command=player_stays)
stay_btn.pack(side="left")

main_window.mainloop()