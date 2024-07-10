# import random
# from board import board
# from cards import draw_card, handle_card, chance_cards, community_chest_cards

# class Player:
#     def __init__(self, name, token=None, properties=None, is_computer=False):
#         self.name = name
#         self.token = token if token is not None else self.tokenSelection()
#         self.money = 1500
#         self.properties = properties if properties is not None else []
#         self.mortgaged_properties = []
#         self.position = 0
#         self.is_computer = is_computer
#         self.in_jail = False
#         self.jail_turns = 0
#         self.get_out_of_jail_free = False
#         self.houses = {}
#         self.hotels = {}

#     def tokenSelection(self):
#         tokens = ["Thor", "Strange", "IronMan", "Hawkeye"]
#         print("Choose your token:")
#         for i, token in enumerate(tokens):
#             print(f"{i + 1}. {token}")
#         choice = int(input("Enter the number of your choice: ")) - 1
#         while choice < 0 or choice >= len(tokens):
#             print("Invalid choice. Please choose again.")
#             choice = int(input("Enter the number of your choice: ")) - 1
#         return tokens[choice]

#     def rollDice(self):
#         die1 = random.randint(1, 6)
#         die2 = random.randint(1, 6)
#         print(f"Hey, you rolled {die1} and {die2}")
#         print(f"You rolled a total of {die1 + die2}")
#         return die1, die2

#     def move(self, roll, players):
#         # If player is in jail, handle jail logic
#         if self.in_jail:
#             print(f"{self.name} is in jail. Options: pay $50, use 'Get Out of Jail Free' card, or roll doubles.")
#             if self.get_out_of_jail_free:
#                 use_card = input("Use 'Get Out of Jail Free' card? (y/n): ").lower()
#                 if use_card == 'y':
#                     self.get_out_of_jail_free = False
#                     self.in_jail = False
#                     print(f"{self.name} used 'Get Out of Jail Free' card.")
#                     self.position = (self.position + roll) % len(board)
#                     return
#             if self.money >= 50:
#                 pay_bail = input("Pay $50 to get out of jail? (y/n): ").lower()
#                 if pay_bail == 'y':
#                     self.money -= 50
#                     self.in_jail = False
#                     print(f"{self.name} paid $50 to get out of jail.")
#                     self.position = (self.position + roll) % len(board)
#                     return
#             die1, die2 = self.rollDice()
#             if die1 == die2:
#                 self.in_jail = False
#                 print(f"{self.name} rolled doubles to get out of jail.")
#                 self.position = (self.position + roll) % len(board)
#                 return
#             self.jail_turns += 1
#             if self.jail_turns >= 3:
#                 self.in_jail = False
#                 self.money -= 50
#                 print(f"{self.name} paid $50 after 3 turns in jail.")
#                 self.position = (self.position + roll) % len(board)
#                 return
#             print(f"{self.name} remains in jail.")
#             return

#         self.position = (self.position + roll) % len(board)
#         current_square = board[self.position]
#         if current_square['name'] == "Go" and self.position != 0:
#             self.money += 200
#             print(f"{self.name} collected $200 for passing GO")

#         if current_square['name'] == "Chance":
#             chance_card = draw_card(chance_cards)
#             handle_card(self, chance_card, players)
#         elif current_square['name'] == "Community Chest":
#             community_chest_card = draw_card(community_chest_cards)
#             handle_card(self, community_chest_card, players)
#         else:
#             print(f"{self.name} moved to square {current_square['square']}: {current_square['name']} (${current_square.get('price', 'N/A')})")

#             if 'price' in current_square:
#                 if current_square not in self.properties and current_square not in self.mortgaged_properties:
#                     print(f"{self.token}, you landed on an unowned property: {current_square['name']}.")
#                 elif current_square in self.properties:
#                     print(f"{self.token}, you landed on your own property: {current_square['name']}.")
#                 elif current_square in self.mortgaged_properties:
#                     print(f"{self.token}, you landed on a mortgaged property: {current_square['name']}.")

#     def buyProperty(self):
#         property = board[self.position]
#         if property not in self.properties and property not in self.mortgaged_properties:
#             if self.money >= property['price']:
#                 self.properties.append(property)
#                 print(f"{self.token} bought {property['name']} for ${property['price']}")
#                 self.money -= property['price']
#                 print(f"Your balance is: {self.money}")
#             else:
#                 print(f"{self.token} does not have enough money to buy {property['name']}")
#         else:
#             print(f"{property['name']} is already owned.")

#     def mortgageProperty(self):
#         if not self.properties:
#             print(f"{self.token}, you do not own any properties.")
#             return

#         print(f"{self.token}, you own the following properties:")
#         for i, property in enumerate(self.properties, 1):
#             print(f"{i}. {property['name']}")

#         choice = int(input("Enter the number of the property you want to mortgage (0 to cancel): "))

#         if choice == 0:
#             return

#         if 1 <= choice <= len(self.properties):
#             property_to_mortgage = self.properties[choice - 1]
#             mortgage_value = property_to_mortgage['price'] // 2

#             self.money += mortgage_value
#             self.mortgaged_properties.append(property_to_mortgage)
#             self.properties.remove(property_to_mortgage)
#             property_to_mortgage['is_mortgaged'] = True

#             print(f"{self.token} mortgaged {property_to_mortgage['name']} for ${mortgage_value}")
#         else:
#             print("Invalid choice.")

#     def payTax(self, amount):
#         self.money -= amount
#         print(f"{self.name} paid ${amount} in taxes. Current balance: ${self.money}")

#     def calculateRent(self, property):
#      if property['name'] in ["Go", "Chance", "Community Chest"]:
#         return 0  # No rent for these special squares
#      elif property in self.properties:
#         return 0  # No rent on own property
#      else:
#         base_rent = property['rent'][0]
#         houses = self.houses.get(property['name'], 0)
#         hotels = self.hotels.get(property['name'], 0)
#         if hotels > 0:
#             return property['rent'][5]
#         return base_rent + houses * (property['rent'][houses] - base_rent)

#     def payRent(self, amount, players):
#         self.money -= amount
#         for player in players:
#             if player != self and board[self.position] in player.properties:
#                 player.money += amount
#                 print(f"{self.name} paid ${amount} in rent to {player.name}. Current balance: ${self.money}")
#                 return

#     def buildHouse(self):
#         property = board[self.position]
#         if property in self.properties and self.money >= 50:
#             self.money -= 50
#             if property['name'] in self.houses:
#                 self.houses[property['name']] += 1
#             else:
#                 self.houses[property['name']] = 1
#             print(f"{self.name} built a house on {property['name']}. Total houses: {self.houses[property['name']]}. Current balance: ${self.money}")
#         else:
#             print(f"{self.name} cannot build a house on {property['name']}")

#     def buildHotel(self):
#         property = board[self.position]
#         if property in self.properties and self.money >= 200:
#             self.money -= 200
#             self.hotels[property['name']] = 1
#             print(f"{self.name} built a hotel on {property['name']}. Total hotels: {self.hotels[property['name']]}. Current balance: ${self.money}")
#         else:
#             print(f"{self.name} cannot build a hotel on {property['name']}")

import random
from board import board
from cards import draw_card, handle_card, chance_cards, community_chest_cards

class Player:
    def __init__(self, name, token=None, properties=None, is_computer=False):
        self.name = name
        self.token = token if token is not None else self.tokenSelection()
        self.money = 1500
        self.properties = properties if properties is not None else []
        self.mortgaged_properties = []
        self.position = 0
        self.is_computer = is_computer
        self.in_jail = False
        self.jail_turns = 0
        self.get_out_of_jail_free = False
        self.houses = {}
        self.hotels = {}

    def tokenSelection(self):
        tokens = ["Thor", "Strange", "IronMan", "Hawkeye"]
        print("Choose your token:")
        for i, token in enumerate(tokens):
            print(f"{i + 1}. {token}")
        choice = int(input("Enter the number of your choice: ")) - 1
        while choice < 0 or choice >= len(tokens):
            print("Invalid choice. Please choose again.")
            choice = int(input("Enter the number of your choice: ")) - 1
        return tokens[choice]

    def rollDice(self):
        die1 = random.randint(1, 6)
        die2 = random.randint(1, 6)
        print(f"Hey, you rolled {die1} and {die2}")
        print(f"You rolled a total of {die1 + die2}")
        return die1, die2

    def move(self, roll, players):
        # If player is in jail, handle jail logic
        if self.in_jail:
            print(f"{self.name} is in jail. Options: pay $50, use 'Get Out of Jail Free' card, or roll doubles.")
            if self.get_out_of_jail_free:
                use_card = input("Use 'Get Out of Jail Free' card? (y/n): ").lower()
                if use_card == 'y':
                    self.get_out_of_jail_free = False
                    self.in_jail = False
                    print(f"{self.name} used 'Get Out of Jail Free' card.")
                    self.position = (self.position + roll) % len(board)
                    return
            if self.money >= 50:
                pay_bail = input("Pay $50 to get out of jail? (y/n): ").lower()
                if pay_bail == 'y':
                    self.money -= 50
                    self.in_jail = False
                    print(f"{self.name} paid $50 to get out of jail.")
                    self.position = (self.position + roll) % len(board)
                    return
            die1, die2 = self.rollDice()
            if die1 == die2:
                self.in_jail = False
                print(f"{self.name} rolled doubles to get out of jail.")
                self.position = (self.position + roll) % len(board)
                return
            self.jail_turns += 1
            if self.jail_turns >= 3:
                self.in_jail = False
                self.money -= 50
                print(f"{self.name} paid $50 after 3 turns in jail.")
                self.position = (self.position + roll) % len(board)
                return
            print(f"{self.name} remains in jail.")
            return

        self.position = (self.position + roll) % len(board)
        current_square = board[self.position]
        if current_square['name'] == "Go" and self.position != 0:
            self.money += 200
            print(f"{self.name} collected $200 for passing GO")

        if current_square['name'] == "Chance":
            chance_card = draw_card(chance_cards)
            handle_card(self, chance_card, players)
        elif current_square['name'] == "Community Chest":
            community_chest_card = draw_card(community_chest_cards)
            handle_card(self, community_chest_card, players)
        else:
            print(f"{self.name} moved to square {current_square['square']}: {current_square['name']} (${current_square.get('price', 'N/A')})")

            if 'price' in current_square:
                if current_square not in self.properties and current_square not in self.mortgaged_properties:
                    print(f"{self.token}, you landed on an unowned property: {current_square['name']}.")
                elif current_square in self.properties:
                    print(f"{self.token}, you landed on your own property: {current_square['name']}.")
                elif current_square in self.mortgaged_properties:
                    print(f"{self.token}, you landed on a mortgaged property: {current_square['name']}.")

    def buyProperty(self):
        property = board[self.position]
        if property not in self.properties and property not in self.mortgaged_properties:
            if self.money >= property['price']:
                self.properties.append(property)
                print(f"{self.token} bought {property['name']} for ${property['price']}")
                self.money -= property['price']
                print(f"Your balance is: {self.money}")
            else:
                print(f"{self.token} does not have enough money to buy {property['name']}")
        else:
            print(f"{property['name']} is already owned.")
        self.checkBankruptcy()

    def mortgageProperty(self):
        if not self.properties:
            print(f"{self.token}, you do not own any properties.")
            return

        print(f"{self.token}, you own the following properties:")
        for i, property in enumerate(self.properties, 1):
            print(f"{i}. {property['name']}")

        choice = int(input("Enter the number of the property you want to mortgage (0 to cancel): "))

        if choice == 0:
            return

        if 1 <= choice <= len(self.properties):
            property_to_mortgage = self.properties[choice - 1]
            mortgage_value = property_to_mortgage['price'] // 2

            self.money += mortgage_value
            self.mortgaged_properties.append(property_to_mortgage)
            self.properties.remove(property_to_mortgage)
            property_to_mortgage['is_mortgaged'] = True

            print(f"{self.token} mortgaged {property_to_mortgage['name']} for ${mortgage_value}")
        else:
            print("Invalid choice.")
        self.checkBankruptcy()

    def payTax(self, amount):
        self.money -= amount
        print(f"{self.name} paid ${amount} in taxes. Current balance: ${self.money}")
        self.checkBankruptcy()

    def calculateRent(self, property):
        if property['name'] in ["Go", "Chance", "Community Chest"]:
            return 0  # No rent for these special squares
        elif property in self.properties:
            return 0  # No rent on own property
        else:
            base_rent = property['rent'][0]
            houses = self.houses.get(property['name'], 0)
            hotels = self.hotels.get(property['name'], 0)
            if hotels > 0:
                return property['rent'][5]
            return base_rent + houses * (property['rent'][houses] - base_rent)

    def payRent(self, amount, players):
        self.money -= amount
        for player in players:
            if player != self and board[self.position] in player.properties:
                player.money += amount
                print(f"{self.name} paid ${amount} in rent to {player.name}. Current balance: ${self.money}")
                break
        self.checkBankruptcy()

    def buildHouse(self):
        property = board[self.position]
        if property in self.properties and self.money >= 50:
            self.money -= 50
            if property['name'] in self.houses:
                self.houses[property['name']] += 1
            else:
                self.houses[property['name']] = 1
            print(f"{self.name} built a house on {property['name']}. Total houses: {self.houses[property['name']]}. Current balance: ${self.money}")
        else:
            print(f"{self.name} cannot build a house on {property['name']}")
        self.checkBankruptcy()

    def buildHotel(self):
        property = board[self.position]
        if property in self.properties and self.money >= 200:
            self.money -= 200
            self.hotels[property['name']] = 1
            print(f"{self.name} built a hotel on {property['name']}. Total hotels: {self.hotels[property['name']]}. Current balance: ${self.money}")
        else:
            print(f"{self.name} cannot build a hotel on {property['name']}")
        self.checkBankruptcy()

    def checkBankruptcy(self):
        if self.money < 0:
            print(f"{self.name} is bankrupt!")
            return True
        return False

    def handleBankruptcy(self, players):
        if self.checkBankruptcy():
            print(f"{self.name} has been removed from the game.")
            players.remove(self)
            if len(players) == 1:
                print(f"{players[0].name} is the winner!")
                return True
        return False