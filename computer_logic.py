# computer_logic.py
from board import *
from cards import draw_card, handle_card, chance_cards, community_chest_cards

def movePlayer(player, roll, players):
    player.move(roll, players)

def computerDecisionToBuy(player):
    property = board[player.position]
    if property not in player.properties and property not in player.mortgaged_properties:
        if player.money >= property['price']:
            player.buyProperty()

def computerDecisionToMortgage(player):
    if player.properties:
        player.mortgageProperty()

def computerTurn(player, players,board,current_square):
    print(f"\n{player.token}'s turn.")
    dice1, dice2 = player.rollDice()
    movePlayer(player, dice1 + dice2, players)
    if current_square['name']== "Go"  and player.position!=0:
            player.money+=200
            print(f"{player.name} collected $200 for passing GO")


    current_square = board[player.position]
    if current_square['name'] == "Chance":
        chance_card = draw_card(chance_cards)
        handle_card(player, chance_card, players)
    elif current_square['name'] == "Community Chest":
        community_chest_card = draw_card(community_chest_cards)
        handle_card(player, community_chest_card, players)
    else:
        property = board[player.position]
        if 'price' in property:
            if property not in player.properties and property not in player.mortgaged_properties:
                if player.money >= property['price']:
                    computerDecisionToBuy(player)

        computerDecisionToMortgage(player)
