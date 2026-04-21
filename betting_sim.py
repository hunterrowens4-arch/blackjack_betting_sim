import json
import random

hands = []

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

def deal_hands(deck): # deal initial hands to player and dealer
    player_hand = [deck.pop()]
    dealer_hand = [deck.pop()]
    player_hand.append(deck.pop())
    dealer_hand.append(deck.pop())
    return player_hand, dealer_hand

def determine_winner(dealer_hand, sdeck, hands, bankroll):
    for hand in hands:
        show_hand('dealer', dealer_hand)
        show_hand('player', hand)
        if sum_hand(hand) > 21:
            print('You bust\n')
        elif sum_hand(dealer_hand) > 21:
            print('Dealer bust, you win!')
            print(f'Paying out: {ibet}\n')
            bankroll += ibet * 2
        elif sum_hand(hand) > sum_hand(dealer_hand):
            print('You win!\n')
            print(f'Paying out: {ibet}\n')
            bankroll += ibet * 2
        elif sum_hand(hand) == sum_hand(dealer_hand):
            print('It\'s a push!\n')
            bankroll += ibet
        else:
            print('Dealer wins!\n')
    return bankroll

def first_action(player_hand, dealer_hand, sdeck, split_no, hands):
    while True:
        print(f'\nDealer Hand: [{dealer_hand[0]}, ?]')
        show_hand('player', player_hand)
        action = input('\nWhat would you like to do? (h/s/d/sp)\n>> ')
        if action == 'h':
            hit(player_hand, sdeck)
            if sum_hand(player_hand) >= 21:
                show_hand('player', player_hand)
        elif action == 's':
            return action, split_no, hands
        elif action == 'd':
            double_down(player_hand, sdeck)
        elif action == 'sp':
            split_no += 1
            hand1, hand2 = split_hand(player_hand, sdeck)
            hands.append(hand1)
            hands.append(hand2)
        else:
            print('Invalid action. Please enter h/s/d/sp.')
            continue
        return action, split_no, hands

def load_json(file_path): # get settings + save data from JSON
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def play_game(): # play hands
    global bankroll, decks, ibet
    hands_played = 0
    print('\nShuffling deck...\n') # initial shuffle to ensure the deck is ready before the first hand
    sdeck = shuffle_deck(decks)
# create loop to allow the player to play multiple hands until they choose to exit
    while True:
        hands = []
        player_hand = []
        dealer_hand = []
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
            hands_played += 1
        player_hand, dealer_hand = deal_hands(sdeck)
        if dealer_hand[0] == 'A':
            print(f'\nDealer Hand: [{dealer_hand[0]}, ?]')
            show_hand('player', player_hand)
            insurance_choice = input('\nDealer shows an Ace. Do you want to take insurance? (y/n)\n>> ').lower().strip()
            if insurance_choice == 'y':
                insurance_bet = int(ibet / 2)
                bankroll -= insurance_bet
                if sum_hand(dealer_hand) == 21:
                    show_hand('dealer', dealer_hand)
                    print('Dealer has blackjack! Insurance bet wins!\n')
                    bankroll += insurance_bet * 2
                    continue
                else:
                    print('Dealer does not have blackjack. Insurance bet lost.\n')
        if sum_hand(player_hand) == 21 and sum_hand(dealer_hand) == 21:
            show_hand('dealer', dealer_hand)
            show_hand('player', player_hand)
            print('It\'s a push!\n')
            bankroll += ibet
            continue
        elif sum_hand(player_hand) == 21:
            print()
            show_hand('dealer', dealer_hand)
            show_hand('player', player_hand)
            print('Blackjack! You win!')
            print(f'Paying out: {int(ibet * 1.5)}\n')
            bankroll += int(ibet * 2.5)
            continue
        elif sum_hand(dealer_hand) == 21:
            show_hand('dealer', dealer_hand)
            show_hand('player', player_hand)
            print('Dealer has blackjack! Dealer wins!\n')
            continue
        resolve_player_hand(player_hand, dealer_hand, sdeck, hands)
        resolve_dealer_hand(dealer_hand, sdeck, player_hand)
        print(' ')
        bankroll = determine_winner(dealer_hand, sdeck, hands, bankroll)

def resolve_dealer_hand(dealer_hand, sdeck, player_hand):
    if sum_hand(player_hand) > 21:
        return
    print('')
    show_hand('dealer', dealer_hand)
    if sum_hand(dealer_hand) >= 17:
        return
    while sum_hand(dealer_hand) < 17:
        hit(dealer_hand, sdeck)
        show_hand('dealer', dealer_hand)

def resolve_player_hand(player_hand, dealer_hand, sdeck, hands):
    split_no = 0
    hands.append(player_hand)
    while True:
        action, split_no, hands = first_action(hands[split_no], dealer_hand, sdeck, split_no, hands)
        if action != 's' and action != 'd':
            subsequent_action(hands[split_no], dealer_hand, sdeck)
        if action != 'sp':
            break

def show_hand(side, hand):
    if sum_hand(hand) == 21:
        print(f'{side.title()} Hand: [{", ".join(hand)}] = 21')
    elif 'A' in hand and sum([values[card] for card in hand]) < 11:
        print(f'{side.title()} Hand: [{", ".join(hand)}] = {sum_hand(hand) - 10} / {sum_hand(hand)}')
    else:
        print(f'{side.title()} Hand: [{", ".join(hand)}] = {sum_hand(hand)}')

def show_help(): # show available commands
    print("""
              Available commands
----------------------------------------------
Play         - Play hands of blackjack
Change Decks - Change the number of decks used
Done         - Exit the program""")

def shuffle_deck(decks): # create and shuffle the deck(s) based on the number of decks chosen
    deck = list(values.keys()) * (4 * decks)
    random.shuffle(deck)
    return deck

def subsequent_action(player_hand, dealer_hand, sdeck):
    if sum_hand(player_hand) >= 21:
        return
    while sum_hand(player_hand) < 21:
        print(f'\nDealer Hand: [{dealer_hand[0]}, ?]')
        show_hand('player', player_hand)
        action = input('What would you like to do? (h/s).\n>> ')
        if action == 'h':
            hit(player_hand, sdeck)
            print(player_hand)
        elif action == 's':
            return
        else:
            print('Invalid action. Please enter (h/s).')

def sum_hand(hand): # helper function to calculate the total value of a hand, accounting for Aces
    total = sum([values[card] for card in hand])
    if 'A' in hand and total <= 11:
        total += 10
    return total

# game actions functions
def double_down(hand, sdeck): # double the bet and take exactly one more card
    global bankroll
    global ibet
    if bankroll < ibet:
        print('Insufficient bankroll to double down.')
        return
    if len(hand) != 2:
        print('You can only double down on your initial hand.')
        return
    bankroll -= ibet
    ibet = ibet * 2
    hand.append(sdeck.pop())
    return

def hit(hand, sdeck): # add a card to the hand
    hand.append(sdeck.pop())

def split_hand(hand, sdeck):
    if hand[0] != hand[1]:
        print('You cannot split this hand. You may only split of both of your cards are the same value.')
        return
    else:
        hand1 = [hand[0], sdeck.pop()]
        hand2 = [hand[1]]
        return hand1, hand2

# list of commands
commands = {
    'change decks': change_decks,
    'help': show_help,
    'play': play_game,
}

# list of in game actions
game_actions = {
    'd': double_down,
    'h': hit,
    'sp': split_hand,
}

settings = load_json('settings.json')
bankroll = settings.get('bankroll', 1000)
decks = settings.get('deck_count', 1)

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