import json
import random

values = {
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    '10': 10,
    'J': 10,
    'Q': 10,
    'K': 10,
    'A': 1
}

# start of functions
def load_json(file_path): # get settings + save data from JSON
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)
settings = load_json("settings.json")
decks = int(settings.get("decks_count", 1))
bankroll = int(settings.get("bankroll", 1000))

def change_decks(): # change the number of decks used in the game
    while True:
        decks_choice = input('How many decks do you want to use? (1/2/4/8)\n>> ')
        try:
            decks = int(decks_choice)
            if decks not in [1, 2, 4, 8]:
                print('Invalid input. Please enter a number (1, 2, 4, or 8).')
                continue
            return decks
        except ValueError:
            print('Invalid input. Please enter a number (1, 2, 4, or 8).')

def show_help(): # show available commands
    print("""
              Available commands
----------------------------------------------
Play         - Play hands of blackjack
Change Decks - Change the number of decks used
Done         - Exit the program
""")

def shuffle_deck(decks): # create and shuffle the deck(s) based on the number of decks chosen
    deck = list(values.keys()) * (4 * decks)
    random.shuffle(deck)
    return deck

def deal_hands(deck): # deal initial hands to player and dealer
    player_hand = [deck.pop()]
    dealer_hand = [deck.pop()]
    player_hand.append(deck.pop())
    dealer_hand.append(deck.pop())
    return player_hand, dealer_hand

def play_game(): # play hands
    global bankroll, decks, ibet
    hands_played = 0
    print('\nShuffling deck...\n') # initial shuffle to ensure the deck is ready before the first hand
    sdeck = shuffle_deck(decks)

# create loop to allow the player to play multiple hands until they choose to exit

    while True:
        bet = input(f'Place your bet (or type "done" to exit)\nBankroll: {bankroll}\n>> ')
        if bet.lower() == 'done':
            print('\nExiting to menu ...')
            break
        try:
            ibet = int(bet)
            if ibet <= 0:
                print('\nInvalid bet. Please enter a positive number.\n')
                continue
            bankroll -= ibet
        except ValueError:
            if bet.lower() == 'done':
                print('\nExiting to menu ...')
                break
            else:
                print('\nInvalid input. Please enter a number for your bet or "done" to exit.')
                continue
        
    # check for remaining cards and shuffle before the hand if the deck is low, then deal
        
        if len(sdeck) < 12:
            print('Shuffling deck...')
            sdeck = shuffle_deck(decks)
        player_hand, dealer_hand = deal_hands(sdeck)
        if dealer_hand[0] == 'A':
            insurance_choice = input('\nDealer shows an Ace. Do you want to take insurance? (y/n)\n>> ').lower().strip()
            if insurance_choice == 'y':
                insurance_bet = int(ibet / 2)
                bankroll -= insurance_bet
                if sum_hand(dealer_hand) == 21:
                    print(f'\nDealer\'s hand: [{dealer_hand[0]}, {dealer_hand[1]}] = 21')
                    print('Dealer has blackjack! Insurance bet wins!\n')
                    bankroll += insurance_bet * 2
                    continue
                else:
                    print('Dealer does not have blackjack. Insurance bet lost.\n')
        if sum_hand(player_hand) == 21 and sum_hand(dealer_hand) == 21:
            print(f'\nDealer\'s hand: [{dealer_hand[0]}, {dealer_hand[1]}] = 21')
            print(f'Your hand: {player_hand} = 21')
            print('It\'s a push!\n')
            bankroll += ibet
            continue
        elif sum_hand(player_hand) == 21:
            print(f'\nDealer\'s hand: [{dealer_hand[0]}, {dealer_hand[1]}] = {sum_hand(dealer_hand)}')
            print(f'Your hand: {player_hand} = 21')
            print('Blackjack! You win!\n')
            bankroll += int(ibet * 2.5)
            continue
        elif sum_hand(dealer_hand) == 21:
            print(f'\nDealer\'s hand: [{dealer_hand[0]}, {dealer_hand[1]}] = 21')
            print(f'Your hand: {player_hand} = {sum_hand(player_hand)}')
            print('Dealer has blackjack! Dealer wins!\n')
            continue

    # loop to allow repeated actions until the player stands or busts

        while sum_hand(player_hand) < 21:
            print(f'\nDealer\'s hand: [{dealer_hand[0]}, ?]')
            if 'A' in player_hand:
                print(f'Your hand: [{", ".join(player_hand)}] = {sum_hand(player_hand) - 10} / {sum_hand(player_hand)}\n')
            else:
                print(f'Your hand: [{", ".join(player_hand)}] = {sum_hand(player_hand)}\n')

        # prompt the player for their action, allowing for all normal blackjack actions, except surrender (hit, stand, double down, split)

            action = input('What would you like to do? (h/s/d/sp)\n>> ').lower().strip()
            if action in game_actions:
                game_actions[action](player_hand, sdeck)
                if action == 'd':
                    break
            elif action == 's':
                break
            else:
                print('Invalid action. Please enter "h", "s", "d", or "sp".')

    # check for busts, if player busted, resolve hand immediately, if not, play out dealer hand and resolve

        if sum_hand(player_hand) > 21:
            print(f'\nYour hand: {player_hand} = {sum_hand(player_hand)}')
            print('You bust! Dealer wins.\n')
            continue

    # play out dealer hand, hitting until 17 or higher, then resolve hand based on standard blackjack rules

        while sum_hand(dealer_hand) < 17:
            hit(dealer_hand, sdeck)
        print(f'\nDealer\'s hand: {dealer_hand} = {sum_hand(dealer_hand)}')
        print(f'Your hand: {player_hand} = {sum_hand(player_hand)}')
        if sum_hand(player_hand) > sum_hand(dealer_hand) or sum_hand(dealer_hand) > 21:
            print('You win!\n')
            if action == 'd':
                bankroll += (ibet * 4)
            else:
                bankroll += (ibet * 2)
        elif sum_hand(player_hand) < sum_hand(dealer_hand):
            print('Dealer wins!\n')
        else:
            print('It\'s a push!\n')
            bankroll += ibet

def sum_hand(hand): # helper function to calculate the total value of a hand, accounting for Aces
    total = sum([values[card] for card in hand])
    if 'A' in hand and total + 10 <= 21:
        total += 10
    return total

# start of the game actions functions
def double_down(hand, sdeck): # double the bet and take exactly one more card
    global bankroll
    if bankroll < ibet:
        print('Insufficient bankroll to double down.')
        return
    if len(hand) != 2:
        print('You can only double down on your initial hand.')
        return
    bankroll -= ibet
    hand.append(sdeck.pop())
    return

def hit(hand, sdeck): # add a card to the hand
    hand.append(sdeck.pop())

# list of commands
commands = {
    'change decks': change_decks,
    'help': show_help,
    'play': play_game,
}

# list of in game actions
game_actions = {
    'd': double_down,
    'h': hit
}

# start main program logic, allowing the user to enter commands until they choose to exit
while True:
    action = input('\nWhat would you like to do?\n>> ').lower().strip()
    if action in commands:
        commands[action]()
    elif action == 'done':
        print('\nExiting the program. Goodbye!')
        with open('settings.json', 'w', encoding='utf-8') as f:
            json.dump({'decks_count': decks, 'bankroll': bankroll}, f, indent=4)
        break
    else:
        print('\nInvalid command. Type "Help" for a list of commands.')