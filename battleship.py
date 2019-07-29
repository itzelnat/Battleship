import random
import sys

class orientation():#Which way the ships will point
     vertical = 'vert'
     horizontal = 'horz'

     def orientations(player):
        return [orientation.vertical, orientation.horizontal]

class ship_location():#Location of the ships
     def __init__(player, row, col):
          player._row = row
          player._col = col

     def __repr__(player):
          return '(%d:%d)' % player.pos()

     def row(player):
          return player._row

     def col(player):
          return player._col

     def pos(player):
          return (player._row, player._col)

class shipinfo():#The ship itself
     def __init__(player, name, size, location, direction):
          player._name = name
          player._size = size
          player._coords = player.findlocations(location, direction)

     def __repr__(player):
          return '{ship: %s size: %d location: %s}' % (player._name, player._size, str(player._coords))

     def findlocations(player, location, direction):
          if direction == orientation.horizontal:
               dRow = 0
               dCol = 1
          else:
               dRow = 1
               dCol = 0

          coords = []
          (row, col) = location.pos()
          for _  in range(player._size):
               coords.append((row, col))
               row += dRow
               col += dCol

          return coords

     def coords(player):
           return player._coords

     def size(player):
           return player._size

     def name(player):
           return player._name

class Status():#The status of the ships

     HIT = 'HIT'
     MISS = 'MISS'
     EMPTY = ''

     def statuses(player):
          return [Status.HIT, Status.MISS, Status.EMPTY]

class game_piece():#The game piece
     def __init__(player, location, ship = None, status = Status.EMPTY):
          player._location = location
          player._ship = ship
          player._status = status

     def __repr__(player):
          return '%d:%d:%s' % (player._location.row(), player._location.col(), player._ship.name() if player._ship != None else '')

     def location(player):
          return player._location

     def ship(player):
          return player._ship

     def status(player):
          return player._status

     def isOccupied(player):
          return player._ship != None

     def ship_to_board(player, ship):
          player._ship = ship

     def setStatus(player, status):
          player._status = status

class Board():#The Game Board
     def __init__(player, rows, cols):
          player._rows = rows
          player._cols = cols
          player._set_ships = player.makeboard()

     def rows(player):
          return player._rows

     def cols(player):
          return player._cols

     def makeboard(player):#Create the game board
          set_ships = []
          for row in range(player._rows):
               set_ships.append([])
               for col in range(player._cols):
                    piece = game_piece(ship_location(row, col))
                    set_ships[row].append(piece)
          return set_ships


     def getship(player, row, col):
          return player._set_ships[row][col]

     def already_there(player, row, col):
          if row < 0 or row >= player._rows or col < 0 or col >= player._cols:
               return False
          return player._set_ships[row][col].ship() != None

     def ship_to_board(player, ship):#Place the ship on the board
          coords = ship.coords()
          for (row, col) in coords:
               piece = player._set_ships[row][col]
               piece.ship_to_board(ship)

          return True

     def displayboard(player, isScan = False):#Display the game board
          print('  ', end = '')
          for col in range(player._cols):
               print('%d ' % (col), end = '')
          print()

          for row in range(player._rows):
               print('%d ' % row, end = '')
               for col in range(player._cols):
                    piece = player._set_ships[row][col]
                    ship = piece.ship()
                    status = piece.status()
                    if status == Status.HIT:
                         print('X ', end = '')
                    elif status == Status.MISS:
                         print('O ', end = '')
                    else:
                         if ship == None or isScan:
                              print('* ' , end = '')
                         else:
                              print('%c ' % ship.name(), end = '')
               print()
          print()

class playgame():#Play the game
     def __init__(player, rows, cols, player1, player2):
          player._rows = rows
          player._cols = cols
          player._player1 = player1
          player._player2 = player2
          player._state1 = current_board(Board(rows, cols))
          player._state2 = current_board(Board(rows, cols))
          player._turn = None
          player._winner = None

     def begin_game(player):#Place the users ships
          player._player1.place(player._state1)
          player._player2.place(player._state2)

          player._turn = player._player1 if not random.randint(0, 1) else player._player2 #Decide whether player1 or player 2 goes first

          while not player._state1.game_over() and not player._state2.game_over():

               if player._turn == player._player1:#Display the board
                    print('Scanning Board')
                    player._state2._board.displayboard(True)
                    print('My Board')
                    player._state1._board.displayboard()

                    player._player1.fire(player._state1, player._state2)

               else:
                    player._player2.fire(player._state2, player._state1)

               player._turn = player._player1 if player._turn == player._player2 else player._player2

          print('Scanning Board')
          player._state2._board.displayboard(True)
          print('My Board')
          player._state1._board.displayboard()

          print()
          if player._state1.total_sunk():
               print('The AI wins.')
          else:
               print('You win!')

class current_board():
     def __init__(player, board):
          player._board = board
          player._ships = {}

     def game_row(player):
          return player._board.rows()

     def game_col(player):
          return player._board.cols()

     def legal_move(player, row, col):
          return row >= 0 and row < player.game_row() and col >= 0 and col < player.game_col()

     def already_fired(player, row, col):
          piece = player._board.getship(row, col)
          return piece.status() == Status.HIT or piece.status() == Status.MISS

     def not_fired(player):
          coords = []
          for row in range(player.game_row()):
               for col in range(player.game_col()):
                    piece = player._board.getship(row, col)
                    if piece.status() == Status.EMPTY:
                         coords.append((row, col))

          return coords

     def not_hit_cheater(player):
           coords = []
           for row in range(player.game_row()):
                   for col in range(player.game_col()):
                           piece = player._board.getship(row, col)
                           if piece.status() == Status.EMPTY and piece.ship() != None:
                                   coords.append((row, col))

           return coords

     def shipcheck(player, ship, onTopDisabled = False):#Check to see if ship placement is valid 
          if ship.name() in player._ships:
               return 'Error symbol %s is already in use. Terminating game' % ship.name()

          if ship.name()[0] in 'xXoO*':
               return 'error symbol. Terminating game.'

          coords = ship.coords()
          for (row, col) in coords:

               if row < 0 or row >= player._board.rows():#Row index out of range
                    return 'Error %s is placed outside of the board. Terminating game.' % ship.name()

               if col < 0 or col >= player._board.cols():#Col index out of range
                    return 'Error %s is placed outside of the board. Terminating game.' % ship.name()

               if player._board.already_there(row, col):#Check if there is a ship placed there already
                    return 'There is already a ship at location %d, %d. Terminating game.' % (row, col)

               if onTopDisabled and (player._board.already_there(row - 1, col) or player._board.already_there(row + 1, col)):
                     return 'Error did not place their ships on top of each other'
          return None

     def ship_to_board(player, ship, onTopDisabled = False):
          error = player.shipcheck(ship, onTopDisabled)
          if error != None:
               return error

          player._board.ship_to_board(ship)
          player._ships[ship.name()] = ship

          return None

     def fire(player, row, col):
          piece = player._board.getship(row, col)
          if piece.ship() != None:
               piece.setStatus(Status.HIT)
          else:
               piece.setStatus(Status.MISS)

          ship = piece.ship()
          if ship != None and player.partial_sunk(ship):
               return 'You sunk my %s' % ship.name()
          elif piece.status() == Status.HIT:
               return 'Hit!'
          else:
               return 'Miss!'

     def partial_sunk(player, ship):#Part of the ship has been hit
          for (row, col) in ship.coords():
               piece = player._board.getship(row, col)
               if piece.status() != Status.HIT:
                    return False
          return True

     def total_sunk(player):#The whole ship has been hit and sunk
          for ship in player._ships.values():
               if not player.partial_sunk(ship):
                    return False
          return True

     def game_over(player):#The game is over
          return player.total_sunk()

class curr_player():
     def __init__(player, name):
          player._name = name

     def name(player):
          return player._name

     def place(player, state):
          pass

     def fire(player, selfState, enemy_board):
          pass

class player_human(curr_player):
     def __init__(player, name, ships):
          curr_player.__init__(player, name)
          player._ships = ships

     def place(player, state):
          for ship in player._ships:
               error = state.ship_to_board(ship)
               if error != None:
                    print(error)
                    sys.exit(0)

     def where_to_fire(player, enemy_board):#Choose where to fire
          while True:
               try:
                    location = input('Enter row and column to fire on separated by a space: ')
                    (row, col) = tuple(int(item) for item in location.split(' '))

                    if row < 0 or row >= enemy_board.game_row():
                         continue

                    if col < 0 or col >= enemy_board.game_col():
                         continue

                    if enemy_board.already_fired(row, col):
                         continue

                    return (row, col)

               except:
                    pass

     def fire(player, selfState, enemy_board):
          (row, col) = player.where_to_fire(enemy_board)
          result = enemy_board.fire(row, col)
          print(result)

class player_randomai(curr_player):#Random AI opponent
     def __init__(player, name, ships):
          curr_player.__init__(player, name)
          player._ships = ships

     def place(player, state):
          ships = sorted(player._ships, key = lambda ship: ship.name())
          player._ships = []

          for ship in ships:
               ship_size = ship.size()
               while True:
                    direction = random.choice(['vert', 'horz'])#Pick which direction
                    if direction == orientation.horizontal:#Starting point
                         row = random.randint(0, state.game_row() - 1)
                         col = random.randint(0, state.game_col() - ship_size)
                    else:
                         row = random.randint(0, state.game_row() - ship_size)
                         col = random.randint(0, state.game_col() - 1)
                         
                    new_ship = shipinfo(ship.name(), ship.size(), ship_location(row, col), direction)
                    error = state.ship_to_board(new_ship, False)
                    if error == None:
                         player._ships.append(new_ship)
                         coords = new_ship.coords()
                         print('Placing ship from %d,%d to %d,%d.' % (coords[0][0], coords[0][1], coords[-1][0], coords[-1][1]))
                         break



     def fire(player, selfState, enemy_board):
          coords = enemy_board.not_fired()
          (row, col) = random.choice(coords)
          result = enemy_board.fire(row, col)
          print('The AI fires at location (%d, %d)' % (row, col))
          print(result)

class player_smartai(player_randomai):#Smart AI, if hit, fire around the area that was hit
     def __init__(player, name, ships):
          curr_player.__init__(player, name)
          player._ships = ships
          player._padding_spots = []

     def fire(player, selfState, enemy_board):
          location = None
          while player._padding_spots:
               (row, col) = player._padding_spots.pop()
               if enemy_board.legal_move(row, col) and not enemy_board.already_fired(row, col):
                    location = (row, col)
                    break

          if not location:
               coords = enemy_board.not_fired()
               location = random.choice(coords)

          (row, col) = location
          result = enemy_board.fire(row, col)
          print('The AI fires at location (%d, %d)' % (row, col))
          print(result)

          if result.find('Hit') != -1 or result.find('sunk') != -1:#Hit occurred
               player._padding_spots.insert(0, (row - 1, col))#Check above
               player._padding_spots.insert(0, (row + 1, col))#Check below
               player._padding_spots.insert(0, (row, col - 1))#Check to the left
               player._padding_spots.insert(0, (row, col + 1))#Check to the right

class player_cheaterai(player_randomai):#Cheater AI, goes row by row firing on the ships
     def __init__(player, name, ships):
          curr_player.__init__(player, name)
          player._ships = ships

     def fire(player, selfState, enemy_board):#AI goes through row by row firing at each ship in the row before going on to the next row that contains a ship
          coords = enemy_board.not_hit_cheater()
          (row, col) = coords[0]
          result = enemy_board.fire(row, col)
          print('The AI fires at location (%d, %d)' % (row, col))
          print(result)		

def int_input(prompt):
     while True:
          try:
               value = int(input(prompt))
               return value
          except:
               pass

def ships_from_file(ship_data_file):#Get ships from user entered file
     file_obj = open(ship_data_file)
     lines = file_obj.readlines()
     file_obj.close()

     ships = []

     for line in lines:
          tokens = line.strip('\r').split(' ')
          symbol = tokens[0]
          row1 = int(tokens[1])
          col1 = int(tokens[2])
          row2 = int(tokens[3])
          col2 = int(tokens[4])

          if row1 != row2 and col1 != col2:
               print('Ships cannot be placed diagonally. Terminating game.')
               sys.exit(0)

          ship = None
          if row1 == row2:
               ship = shipinfo(symbol, abs(col2 - col1) + 1, ship_location(row1, min(col1, col2)), orientation.horizontal)
          else:
               ship = shipinfo(symbol, abs(row2 - row1) + 1, ship_location(min(row1, row2), col1), orientation.vertical)
          ships.append(ship)
     return ships

def chooseai():#Choose which AI to face
     while True:
          ai_type = int_input("""Choose your AI.\n1. Random\n2. Smart\n3. Cheater\n Your choice: """)
          if ai_type >= 1 and ai_type <= 3:
               return ai_type

if __name__ == "__main__":
     init_seed = int_input('Enter the seed: ')#Choose random seed
     while True:
        width = int_input('Enter the width of the board: ')#Board width
        if width > 0:
             break
     while True:#Board height
        height = int_input('Enter the height of the board: ')
        if height > 0:
             break
     ship_data_file = ''
     while True:
          try:
               ship_data_file = input('Enter the name of the file containing your ship placements: ')
               if FileNotFoundError:
                    break
          except:
               pass
     ai_type = chooseai()#Choose which AI to play against
     ships = ships_from_file(ship_data_file)#Get the ships from the file
     player1 = player_human('My', ships)#Create player 1
     player2 = None#Create player 2
     if ai_type == 1:
          player2 = player_randomai('RandomAI', ships)
     elif ai_type == 2:
          player2 = player_smartai('SmartAI', ships)
     else:
          player2 = player_cheaterai('CheaterAI', ships)

     random.seed(init_seed)#Initialize seed
     game = playgame(height, width, player1, player2)#Create the game
     game.begin_game()#Start playing the game
