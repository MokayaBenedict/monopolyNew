# main.py
from player import Player
from computer_logic import computerTurn
from board import board
import random

def movePlayer(player, roll, players):
    player.move(roll, players)

def play_game():
    global player1, player2, players
    print("Player 1, please select your token.")
    player1 = Player("Player 1")
    remaining_tokens = ["Thor", "Strange", "IronMan", "Hawkeye"]
    remaining_tokens.remove(player1.token)
    player2 = Player("Computer", token=random.choice(remaining_tokens), is_computer=True)
    players = [player1, player2]

    current_player = player1

    while True:
        current_square = board[current_player.position] 

        if current_player.is_computer:
            computerTurn(current_player, players, board, current_square)
        else:
            print(f"\n{current_player.token}'s turn.")
            input("Press Enter to roll the dice.\n")
            dice1, dice2 = current_player.rollDice()
            movePlayer(current_player, dice1 + dice2, players)

            property = board[current_player.position]
            if 'price' in property:
                if property not in current_player.properties and property not in current_player.mortgaged_properties:
                    print(f"\n{current_player.token}, do you want to buy {property['name']} for ${property['price']}?")
                    buy_option = input("Press 'y' to buy or 'n' to skip: ").lower()
                    if buy_option == 'y':
                        current_player.buyProperty()

            print(f"\n{current_player.token}, do you want to mortgage a property?")
            mortgage_option = input("Press 'y' to mortgage or 'n' to continue: ").lower()
            if mortgage_option == 'y':
                current_player.mortgageProperty()

        current_player = player1 if current_player == player2 else player2

play_game()