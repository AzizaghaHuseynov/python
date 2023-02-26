import pygame
import sys
import time
from SaveLoadManager import SaveLoadSystem

pygame.init()




black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
light_green = (0, 125, 0)
brown = (92, 64, 51)
light_brown = (100, 154, 122)

font = pygame.font.SysFont(None, 25)

# drawing tile circles
center = 37
radius = 30

saveloadmanager = SaveLoadSystem(".save", "save_data")



def making_board(screen):
    square = 75
    # 8x8 game board
    for row in range(8):
        for column in range(8):
            if (row + column) % 2 == 0:
                color = light_green
            else:
                color = green
            pygame.draw.rect(screen, color, (row * square, column * square, square, square))
    pygame.display.update()


def making_tiles(screen, board):
    global color
    for row in range(8):
        for column in range(8):
            if board[row][column] == "":
                continue
            elif board[row][column] == "White":
                color = white
            elif board[row][column] == "Black":
                color = black

            # print(f"drawing at {row, column}  for {color}")
            pygame.draw.circle(screen, color, (column * 75 + center, row * 75 + center), radius)
    pygame.display.update()


def possible_move_drawing(screen, row, column): # white circles
    rad = 10
    pygame.draw.circle(screen, white, (row * 75 + center, column * 75 + center), rad)
    pygame.display.update()












class Board:
    global possible_moves
    def __init__(self):
        # 8x8 Grid
        self.grid = [[''] * 8 for _ in range(8)]

    def get_possible_moves(self, player):
        possible_moves = []
        # Loop through all spots on the board and check if each one is possible to play
        # for a given player
        for row_ind, row in enumerate(self.grid):
            # print(f"row_ind: {row_ind}, row: {row}")
            for column_ind, column in enumerate(row):
                move = row_ind, column_ind
                # print(f"column_ind: {column_ind}, column: {column}")
                if self.possible_move((row_ind, column_ind), player):  # I say if those row and column indexes have White or Black player, append those column and row indexes inside of possible_moves
                    possible_moves.append((move)) # it counts rows and columns by adding direction and when it sees that there is a player in that row and column cordination,
                    print(f"fdsa: {possible_moves}")

        if len(possible_moves) == 0:
            possible_moves.append((-1, -1))
        # print(f"Possible moves: {possible_moves}")
        return possible_moves

    def possible_move(self, move, player):
        row, column = move  # this is all columns' and rows' coordinates as a tuple
        if self.grid[row][column] in ["Black", "White"]: # Can't play a move on a taken space
            #print(self.grid[row][column])
            return False

        #  Check up down left right and all diagonals
        directions = [[0, -1], [1, -1], [1, 0], [1, 1], [0, 1], [-1, 1], [-1, 0], [-1, -1]]
        for direction in directions:
            print(f"dir: {direction}")
            # If any direction is possible then the move is playable
            if self.played_direction(move, direction, player): # calling played dir func.
                return True
        return False

    def played_direction(self, move, direction, player):
        if player == 'White':
            opponent = 'Black'
        else:
            opponent = 'White'


        # Number of opponent tiles in between your move and one of your own pieces
        row, column = move
        print(f"move: {move}")
        opponent_tiles = 0
        while True:
            # Move along board depending on current direction
            row += direction[0]
            column += direction[1]
            print(f"roww: {row}")
            print(f"columnn: {column}")

            # Can not go farther than length of board
            if (row > 7 or row < 0) or (column > 7 or column < 0):
                break
            # There can not be a space in the middle of a move
            elif self.grid[row][column] == '':
                break
            # Opponents tiles must be between your two pieces
            elif self.grid[row][column] == opponent:
                opponent_tiles += 1
            # There must be one of your own tiles across from your move
            elif self.grid[row][column] == player:
                # There must be at least one opponent tiles in between your own pieces
                if opponent_tiles > 0:
                    return True
                else:
                    break

    def flip_tiles(self, move, player):
        if player == 'White':
            opponent = 'Black'
        else:
            opponent = 'White'


        row, column = move
        print(f"move: {move}")
        directions = [[0, -1], [1, -1], [1, 0], [1, 1], [0, 1], [-1, 1], [-1, 0], [-1, -1]]

        for direction in directions:
            print(f"direc: {direction}")
            if self.played_direction(move, direction, player): #if this statement(played direction function works, i simply play forward by adding rows in direction to the directions
                while True:
                    row += direction[0]
                    print(f"roww: {row}")
                    column += direction[1]
                    print(f"columnn: {column}")

                    if (row > 7 or row < 0) or (column > 7 or column < 0):
                        break
                    elif self.grid[row][column] == player:
                        break
                    elif self.grid[row][column] == opponent:
                        self.grid[row][column] = player
            row, column = move

class Player:
    def __init__(self, symbol):
        self.symbol = symbol

    def get_move(self, possible_moves, loc):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    saveloadmanager.save_game_data([loc], ["game_board"])
                    sys.exit()
                # Check for left click to select a move
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == True:
                    x, y = pygame.mouse.get_pos()
                    board_row = y // 75
                    board_column = x // 75
                    if (board_row, board_column) in possible_moves:
                        # print(f"played move: {board_row, board_column}")  # shows where I played
                        return board_row, board_column

    def update_tile_count(self, player, board):
        self.tile_count = 0
        for i in board:
            self.tile_count += i.count(player)
        # print(f"self.tile_count: {self.tile_count}", end=" ")  # counts white and black tiles



class Game:
    def __init__(self, board):
        self.width = 600
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))

        self.board = board
        self.turn = 0
        self.player_one = Player("White")
        self.player_two = Player("Black")
        self.possible_moves = []




    def display_possible_moves(self):
        # Draws the white circle at a possible move
        for possible_move in self.possible_moves:
            possible_move_drawing(self.screen, possible_move[1], possible_move[0])
            # print(f"tuple x and y's: {possible_move[0]}")

    def update_board(self):
        making_board(self.screen)
        making_tiles(self.screen, self.board.grid)

    def set_up_board(self):
        # Each player starts with two pieces in the middle
        self.update_board()



    def button_adding(self, msg, color, buttonx, buttony, buttonwidth, buttonheight):
        self.text_surface, self.text_rect = self.text_objects(msg, color)
        self.text_rect.center = ((buttonx + (buttonwidth / 2)), buttony + (buttonheight / 2))
        self.screen.blit(self.text_surface, self.text_rect)

    def text_objects(self, text, color):
        self.text_surface = font.render(text, True, color)
        return self.text_surface, self.text_surface.get_rect()

    def button(self, text, x, y, width, height, inactive_color, active_color, action=None):
        cur = pygame.mouse.get_pos()
        # print(cur)
        click = pygame.mouse.get_pressed()
        # print(click)
        if x + width > cur[0] > x and y + height > cur[1] > y:
            pygame.draw.rect(self.screen, active_color, (x, y, width, height))
            if click[0] and action != None:
                if action == "Quit":
                    pygame.quit()
                    quit()
                if action == "Rematch":
                    game_board = Board()
                    game = Game(game_board)
                    game.main()
                # print("Button clicked!!!")
        else:
            pygame.draw.rect(self.screen, inactive_color, (x, y, width, height))
        self.button_adding(text, black, x, y, width, height)

    def message_to_screen(self, msg, color, x_displace=0, y_displace=0):
        self.text_surface, self.text_rect = self.text_objects(msg, color)
        self.text_rect.center = self.width / 2 + x_displace, self.height / 2 + y_displace
        self.screen.blit(self.text_surface, self.text_rect)

    def display_winner(self):
        game_over = True

        loc = [(0, 0)]*65
        loc[27] = loc[28] = (2, 2)
        loc[35] = loc[36] = (1, 1)
        saveloadmanager.save_game_data([loc], ["game_board"])
        while game_over:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            self.screen.fill(light_green)
            pygame.draw.rect(self.screen, green, (112.5, 175, 375, 175))  # pop up
            pygame.draw.rect(self.screen, white, (170, 310, 100, 30))  # 2 recs below
            pygame.draw.rect(self.screen, white, (340, 310, 100, 30))  # 2 recs below
            pygame.draw.rect(self.screen, white, (175, 185, 250, 30))  # game over background color
            pygame.draw.rect(self.screen, white, (200, 225, 200, 50))  # table background color
            pygame.draw.rect(self.screen, black, (200, 225, 1, 50))  # drawing table
            pygame.draw.rect(self.screen, black, (200, 225, 200, 1))  # drawing table
            pygame.draw.rect(self.screen, black, (200, 275, 200, 1))  # drawing table
            pygame.draw.rect(self.screen, black, (400, 225, 1, 50))  # drawing table

            self.message_to_screen("Game Over", black, 0, -100)
            # self.message_to_screen("Rematch", black, -80, 25)
            # self.message_to_screen("Quit", black, 90, 25)
            self.button("Rematch", 170, 310, 100, 30, white, light_brown, action="Rematch")
            self.button("Quit", 340, 310, 100, 30, white, light_brown, action="Quit")

            if self.player_one.tile_count > self.player_two.tile_count:
                self.message_to_screen("Player 1 is winner!", black, 0, -10)
                self.message_to_screen(f"Player 1 White tiles  {self.player_one.tile_count}", black, 0, -60)
                self.message_to_screen(f"Player 2 Black tiles  {self.player_two.tile_count}", black, 0, -40)
            elif self.player_one.tile_count < self.player_two.tile_count:
                self.message_to_screen("Player 2 is winner!", black, 0, -10)
                self.message_to_screen(f"Player 1 White tiles  {self.player_one.tile_count}", black, 0, -60)
                self.message_to_screen(f"Player 2 Black tiles  {self.player_two.tile_count}", black, 0, -40)

            pygame.display.update()

    def main(self):
        loc = [None] * 65
        # print(f"loc: {loc}")
        load_loc = saveloadmanager.load_game_data(["game_board"], [[]])
        for i in range(0, 64):
            row = int(i/8)
            # print(f"rowww: {row}")
            column = i - row*8
            # print(f"columnnn: {column}")
            if load_loc[i] == (0, 0):
                self.board.grid[row][column] = ''
            elif load_loc[i] == (1, 1):
                self.board.grid[row][column] = 'White'
            else:
                self.board.grid[row][column] = 'Black'

        # if load_loc[64] == (1, 1):
        #     current_player = 'White'
        # else:
        #     current_player = 'Black'
        self.set_up_board()
        # flg = 1

        while True:
            for i in range(0, 8):
                for j in range(0, 8):
                    if self.board.grid[i][j] == '':
                        loc[i*8+j] = (0, 0)
                    elif self.board.grid[i][j] == 'White':
                        loc[i*8+j] = (1, 1)
                    else:
                        loc[i*8+j] = (2, 2)






            if self.possible_moves == [(-1, -1)]:
                time.sleep(1)
                self.display_winner()


            if self.turn % 2 == 0:
                current_player = 'White'

                # row "current_player = 'White'" must be deleted to uncomment code below

                # print(f"self.turn: {self.turn}")
                # if flg == 0:
                #     current_player = 'White'
                # else:
                #     if load_loc[64] == (1, 1):
                #         current_player = 'White'
                #     flg = 0
                # loc[64] = (1, 1)


                self.possible_moves = self.board.get_possible_moves('White')






                if self.possible_moves == [(-1, -1)]:

                    time.sleep(1)
                    self.display_winner()
                self.display_possible_moves()
                move = self.player_one.get_move(self.possible_moves, loc)


            else:
                current_player = 'Black'

                # row "current_player = 'Black'" must be deleted to uncomment code below

                # if flg == 0:
                #     current_player = 'Black'
                # else:
                #     if load_loc[64] == (2, 2):
                #         current_player = 'Black'
                #
                #     flg = 0
                # loc[64] = (2, 2)


                self.possible_moves = self.board.get_possible_moves('Black')






                if self.possible_moves == [(-1, -1)]:
                    time.sleep(1)
                    self.display_winner()
                self.display_possible_moves()
                move = self.player_two.get_move(self.possible_moves, loc)




            self.board.grid[move[0]][move[1]] = current_player # here, i make tile appear on screen
            self.board.flip_tiles(move, current_player) # flips the tile on screen

            # Update the tile counts to check for a win
            self.player_one.update_tile_count('White', self.board.grid)
            self.player_two.update_tile_count('Black', self.board.grid)

            # Reset possible for next turn
            self.update_board()
            self.turn += 1



game_board = Board()
game = Game(game_board)
game.main()


