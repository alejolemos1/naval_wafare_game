# Import time to schedule breaks between outings
import time

# Declaring the classes that make up our game
class Ship:
    def __init__(self, name, size, symbol):
        self.name = name
        self.size = size
        self.symbol = symbol
    
class Destroyer(Ship):
    def __init__(self, name = 'Destroyer', size = 2, symbol = 'D'):
        super().__init__(name, size, symbol)
        self.has_special_attack = None

class Submarine(Ship):
    def __init__(self, name = 'Submarine', size = 3, symbol = 'S'):
        super().__init__(name, size, symbol)
        self.has_special_attack = 'Show a enemy box'
    def special_attack(self, player, enemy):
        print('Showing a enemy box...')
        while True:
            try:
                row = int(input('Select the row: ')) -1
                if row in range(8):
                    break
                else:
                    print('Error: Insert a row between 1 and 8')
            except ValueError:
                print('Error: Invalid row')
        while True:
            try:
                column = int(input('Select the column: ')) -1
                if column in range(8):
                    break
                else:
                    print('Error: Insert a column between 1 and 8')
            except ValueError:
                print('Error: Invalid column')
        enemy.public_matrix[row][column] = enemy.real_matrix[row][column]
        enemy.print_public_matrix()

class BattleShip(Ship):
    def __init__(self, name = 'Battleship', size = 4, symbol = 'B'):
        super().__init__(name, size, symbol)
        self.has_special_attack = '1 extra shoot'
    def special_attack(self, player, enemy):
        print('1 extra shoot...')
        player.attack(enemy)

class Player:
    def __init__(self, name):
        self.name = name
        self.real_matrix = [['  ' for column in range(8)] for row in range(8)]
        self.public_matrix = [['//' for column in range(8)] for row in range(8)]
    def print_matrix(self):
        print('-'*24)
        for row in self.real_matrix:
            for box in row:
                print(box, end=' ')
            print()
        print('-'*24)
    def print_public_matrix(self):
        print('-'*24)
        for row in self.public_matrix:
            for box in row:
                print(box, end=' ')
            print()
        print('-'*24)

    def insert_ship(self, ship):
        print(f"Placing the {ship.name}...")
        while True:
            try:
                initial_row = int(input("Insert the initial row: ")) -1
                if initial_row in range(8):
                    break
                else:
                    print('Error: Insert a row between 1 and 8')
            except ValueError:
                print('Error: Invalid row')
        while True:
            try:
                initial_column = int(input("Insert the initial column: ")) -1
                if initial_column in range(8) and \
                self.real_matrix[initial_row][initial_column] == '  ' and \
                (initial_row + ship.size -1 < 8 or initial_column + ship.size -1 < 8):
                    break
                else:
                    if initial_column not in range(8):
                        print('Error: Insert a column between 1 and 8')
                    elif self.real_matrix[initial_row][initial_column] != '  ':
                        print('Occupied box')
                    elif initial_row + ship.size -1 > 7 and initial_column + ship.size -1 > 7:
                        print('Insufficient space')
            except ValueError:
                print('Error: Invalid column')
        while True:
            orientation = input("Select the orientation, vertical (V) or horizontal (H): ").upper()
            if orientation == 'V' and initial_row + ship.size -1 < 8:
                if all(self.real_matrix[initial_row + i][initial_column] == '  ' for i in range(ship.size -1)):
                    for row in range(ship.size):
                        self.real_matrix[initial_row + row][initial_column] = ship.symbol
                    break
                else:
                    print('Error: The space is already occupied')
            elif orientation == 'H' and initial_column + ship.size -1 < 8:
                if all(self.real_matrix[initial_row][initial_column + i] == '  ' for i in range(ship.size -1)):
                    for column in range(ship.size):
                        self.real_matrix[initial_row][initial_column + column] = ship.symbol
                    break
                else:
                    print('Error: The space is already occupied')
            else:
                if orientation != 'V' and orientation != 'H':
                    print('Invalid orientation')
                elif initial_row + ship.size -1 > 8:
                    print('Insufficient space')
    def attack(self, enemy):
        while True:
            try:
                row = int(input('Select the row: ')) -1
                if row in range(8):
                    break
                else:
                    print('Error: Insert a row between 1 and 8')
            except ValueError:
                print('Error: Invalid row')
        while True:
            try:
                column = int(input('Select the column: ')) -1
                if column in range(8):
                    break
                else:
                    print('Error: Insert a column between 1 and 8')
            except ValueError:
                print('Error: Invalid column')
        if enemy.real_matrix[row][column] != '  ' and enemy.real_matrix[row][column] != '##':
            enemy.real_matrix[row][column] = enemy.public_matrix[row][column] = '##'
            enemy.print_public_matrix()
            print(f'Hit! There was a ship\n{'-'*24}')
        else:
            if enemy.real_matrix[row][column] == '  ':
                enemy.public_matrix[row][column] = '  '
                enemy.print_public_matrix()
                print(f'Water!\n{'-'*24}')
            elif enemy.real_matrix[row][column] == '##':
                enemy.print_public_matrix()
                print(f'Ship ruins!\n{'-'*24}')
    def check_empty_matrix(self):
        for row in self.real_matrix:
            for box in row:
                if box != '  ' and box != '##':
                    return False
        return True

# Starting the game
def start_game():
    print('Welcome to Naval Warfare')
    player_1 = Player('Player 1')
    player_2 = Player('Player 2')

    player_1_ships = [
        Destroyer(symbol = 'D1'),
        Submarine(symbol = 'S1'),
        BattleShip(symbol = 'B1')
    ]
    player_2_ships = [
        Destroyer(symbol = 'D2'),
        Submarine(symbol = 'S2'),
        BattleShip(symbol = 'B2')
    ]
    
    print('Player 1 places his ships on his map (8x8)')
    for ship in player_1_ships:
        player_1.insert_ship(ship)

    player_1.print_matrix()

    print('Player 2 places his ships on his map')
    for ship in player_2_ships:
        player_2.insert_ship(ship)
    
    player_2.print_matrix()

    is_player1_map_empty = False
    is_player2_map_empty = False

    game_ships = [ship for pair in zip(player_1_ships, player_2_ships) for ship in pair]

    while not is_player1_map_empty and not is_player2_map_empty:
        for ship in game_ships:
            if '1' in ship.symbol:
                print(f'Player 1 attacks with the {ship.name}...')
                player_1.attack(player_2)
                time.sleep(0.45)
                if ship.has_special_attack != None:
                    ship.special_attack(player_1, player_2)
                    time.sleep(0.45)
            elif '2' in ship.symbol:
                print(f'Player 2 attacks with the {ship.name}...')
                player_2.attack(player_1)
                time.sleep(0.45)
                if ship.has_special_attack != None:
                    ship.special_attack(player_2, player_1)
                    time.sleep(0.45)
            
            is_player1_map_empty = player_1.check_empty_matrix()
            is_player2_map_empty = player_2.check_empty_matrix()

    if is_player1_map_empty == True and is_player2_map_empty == True:
        print("Tie!!\nRestarting game...")
        start_game()
    elif is_player1_map_empty == False and is_player2_map_empty == True:
        print('Player 1 wins')
    else:
        print('Player 2 wins')
        

    

start_game()