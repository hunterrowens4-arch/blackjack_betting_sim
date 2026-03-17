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
    hands_played = 0
    print('\nShuffling deck...\n') # initial shuffle to ensure the deck is ready before the first hand
    sdeck = shuffle_deck(decks)

# create loop to allow the player to play multiple hands until they choose to exit

    while True:
        bet = input('Place your bet (or type "done" to exit)\n>> ')
        if bet.lower() == 'done':
            print('\nExiting to menu ...')
            break
        try:
            ibet = int(bet)
            if ibet <= 0:
                print('\nInvalid bet. Please enter a positive number.\n')
                continue
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
        if sum([values[card] for card in player_hand]) == 21 and sum([values[card] for card in dealer_hand]) == 21:
            print(f'\nDealer\'s hand: [{dealer_hand[0]}, {dealer_hand[1]}] = 21')
            print(f'Your hand: {player_hand} = 21')
            print('It\'s a push!\n')
            continue

    # loop to allow repeated actions until the player stands or busts

        while sum([values[card] for card in player_hand]) < 21:
            print(f'\nDealer\'s hand: [{dealer_hand[0]}, ?]')
            print(f'Your hand: [{", ".join(player_hand)}] = {sum([values[card] for card in player_hand])}\n')

        # prompt the player for their action, allowing for all normal blackjack actions, except surrender (hit, stand, double down, split)

            action = input('What would you like to do? (h/s/d/sp)\n>> ').lower().strip()
            if action in game_actions:
                game_actions[action](player_hand, sdeck)
            elif action == 's':
                break
            else:
                print('Invalid action. Please enter "h", "s", "d", or "sp".')

    # check for busts, if player busted, resolve hand immediately, if not, play out dealer hand and resolve

        if sum([values[card] for card in player_hand]) > 21:
            print(f'\nYour hand: {player_hand} = {sum([values[card] for card in player_hand])}')
            print('You bust! Dealer wins.\n')
            continue

    # play out dealer hand, hitting until 17 or higher, then resolve hand based on standard blackjack rules

        while sum([values[card] for card in dealer_hand]) < 17:
            hit(dealer_hand, sdeck)
        print(f'\nDealer\'s hand: {dealer_hand} = {sum([values[card] for card in dealer_hand])}')
        print(f'Your hand: {player_hand} = {sum([values[card] for card in player_hand])}')
        if sum([values[card] for card in player_hand]) > sum([values[card] for card in dealer_hand]) or sum([values[card] for card in dealer_hand]) > 21:
            print('You win!\n')
        elif sum([values[card] for card in player_hand]) < sum([values[card] for card in dealer_hand]):
            print('Dealer wins!\n')
        else:
            print('It\'s a push!\n')

# start of the game actions functions
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
    'h': hit
}

# start main program logic, allowing the user to enter commands until they choose to exit
while True:
    action = input('\nWhat would you like to do?\n>> ').lower().strip()
    if action in commands:
        commands[action]()
    elif action == 'done':
        print('\nExiting the program. Goodbye!')
        break
    else:
        print('\nInvalid command. Type "Help" for a list of commands.')