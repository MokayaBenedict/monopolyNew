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
        self.houses = 0
        self.hotels = 0

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
        self.position = (self.position + roll) % len(board)
        current_square = board[self.position]
        if current_square['name']== "Go"  and self.position!=0:
            self.money+=200
            print(f"{self.name} collected $200 for passing GO")

        if current_square['name'] == "Chance" and current_square['price']==0:
            chance_card = draw_card(chance_cards)
            handle_card(self, chance_card, players)
        elif current_square['name'] == "Community Chest" and current_square['price']==0:
            community_chest_card = draw_card(community_chest_cards)
            handle_card(self, community_chest_card, players)
        else:
            print(f"{self.name} moved to square {current_square['square']}: {current_square['name']} (${current_square.get('price', 'N/A')})")

            if 'price' in current_square:
                if current_square not in self.properties and current_square not in self.mortgaged_properties:
                    # Handle unowned property
                    print(f"{self.token}, you landed on an unowned property: {current_square['name']}.")
                    self.handlePropertyPurchase(current_square)
                elif current_square in self.properties:
                    # Handle owned property
                    self.handleRentPayment(current_square, players)
                elif current_square in self.mortgaged_properties:
                    # Handle mortgaged property
                    print(f"{self.token}, you landed on a mortgaged property: {current_square['name']}.")

    def handlePropertyPurchase(self, property):
        print(f"{self.token}, do you want to buy {property['name']} for ${property['price']}?")
        buy_option = input("Press 'y' to buy or 'n' to skip: ").lower()
        if buy_option == 'y':
            self.buyProperty(property)

    def buyProperty(self, property):
        if self.money >= property['price']:
            self.properties.append(property)
            print(f"{self.token} bought {property['name']} for ${property['price']}")
            self.money -= property['price']
            print(f"Your balance is: {self.money}")
        else:
            print(f"{self.token} does not have enough money to buy {property['name']}")

    def handleRentPayment(self, property, players):
        owner = self.findPropertyOwner(property, players)
        if owner and owner != self:
            rent_amount = self.calculateRent(property)
            print(f"{self.token}, you owe ${rent_amount} rent to {owner.token}.")
            if self.money >= rent_amount:
                self.money -= rent_amount
                owner.money += rent_amount
                print(f"Payment successful.")
            else:
                self.handleBankruptcy(players)
        else:
            print(f"{self.token}, you landed on your own property: {property['name']}.")

    def calculateRent(self, property):
        base_rent = property.get('rent', 0)
        if 'house_price' in property and 'hotel_price' in property:
            total_buildings = self.houses + self.hotels
            return base_rent + total_buildings * property['rent_increment']
        return base_rent

    def findPropertyOwner(self, property, players):
        for player in players:
            if property in player.properties:
                return player
        return None

    def handleBankruptcy(self, players):
        print(f"{self.token} is bankrupt!")
        # Remove player from the game
        players.remove(self)
        # Transfer properties to the bank or auction them
        self.sellProperties(players)

    def sellProperties(self, players):
        for property in self.properties[:]:  # Iterate over a copy of the list
            self.properties.remove(property)
            # Transfer property to the bank or auction it
            print(f"{property['name']} has been returned to the bank.")

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

    def buyHouse(self, property):
        if property in self.properties and self.money >= property.get('house_price', 0):
            self.houses += 1
            self.money -= property['house_price']
            print(f"{self.token} bought a house on {property['name']}.")

    def buyHotel(self, property):
        if property in self.properties and self.money >= property.get('hotel_price', 0):
            self.hotels += 1
            self.money -= property['hotel_price']
            print(f"{self.token} bought a hotel on {property['name']}.")
