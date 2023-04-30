# Imports
import pygame as pg
import random
import sys

# Classes


class GameBoard:
    def __init__(self, player1, player2):
        self._tiles = []
        self._players = [player1, player2]
        self._turn_manager = TurnManager()
        self._screen_width = 1600
        self._screen_height = 1000
        self._base_margin = 30
        self._box_color = (171, 117, 46)
        self._surface_color = (247, 236, 200)
        self._screen = pg.display.set_mode(
            (self._screen_width, self._screen_height))
        self._screen.fill(self._box_color)

    def paint(self):
        for tile in self._tiles:
            tile.paint(self._screen)

    def move_stone(self, tile_from, tile_to):
        tile_to.add_stone(tile_from._stones.last())
        tile_from.remove_stone()


class Tile:
    def __init__(self, pos_x, pos_y, size, color):
        self._stones = []
        self._white_color = (133, 78, 35)
        self._black_color = (107, 74, 53)
        self._size = size
        self._color = color
        self._pos_x = pos_x
        self._pos_y = pos_y
        self._height_multiplier = 3

    def add_stone(self, stone):
        self._stones.append(stone)

    def remove_stone(self):
        self._stones.last().remove()

    def paint(self, screen):
        tileDirection = self._size*self._height_multiplier if self._pos_y is 0 else - \
            self._size*self._height_multiplier
        points = [[self._pos_x, self._pos_y],
                  [self._pos_x + self._size / 2, self._pos_y + tileDirection],
                  [self._pos_x + self._size, self._pos_y]]

        pg.draw.polygon(
            screen, self._white_color if self._color is "White" else self._black_color, points)

        for num in range(len(self._stones)):
            self._stones[num].paint(screen, self._pos_x,
                                    self._pos_y, num, self._size/2, True if self._pos_y is 0 else False)


class Stone:
    def __init__(self, player):
        self._white_color = (255, 255, 255)
        self._black_color = (0, 0, 0)
        self._player = player
        self._base_radius = 40

    def paint(self, board, pos_x, pos_y, num, pos_x_shift, direction):
        y_shifted = (pos_y + (2*self._base_radius)*(num)+self._base_radius) if direction else (
            pos_y + (2*self._base_radius)*(-num)-self._base_radius)
        color = self._white_color if self._player._color is "White" else self._black_color
        pg.draw.circle(board, color, (pos_x + pos_x_shift,
                       y_shifted), self._base_radius)


class Dice:
    def __init__(self, pos_x, pos_y):
        self._number = 1
        self._base_size = 100
        self._dot_base_size = 10
        self._pos_x = pos_x-self._base_size/2
        self._pos_y = pos_y-self._base_size/2

    def throw(self, rand_from, rand_to):
        self._number = random.randint(rand_from, rand_to)

    def paint(self, board):
        pg.draw.rect(board, "White", [
                     self._pos_x, self._pos_y, self._base_size, self._base_size])
        match self._number:
            case 1:
                self.paint_one(board)
            case 2:
                self.paint_two(board)
            case 3:
                self.paint_one(board)
                self.paint_two(board)
            case 4:
                self.paint_two(board)
                self.paint_four(board)
            case 5:
                self.paint_one(board)
                self.paint_two(board)
                self.paint_four(board)
            case 6:
                self.paint_four(board)
                self.paint_two(board)
                self.paint_six(board)

    def paint_one(self, board):
        pg.draw.circle(board, "Black", [
                       self._pos_x + self._base_size/2, self._pos_y + self._base_size/2], self._dot_base_size)

    def paint_two(self, board):
        pg.draw.circle(board, "Black", [
                       self._pos_x + self._base_size/5, self._pos_y + self._base_size/5], self._dot_base_size)
        pg.draw.circle(board, "Black", [
                       self._pos_x + self._base_size/5*4, self._pos_y + self._base_size/5*4], self._dot_base_size)

    def paint_four(self, board):
        pg.draw.circle(board, "Black", [
                       self._pos_x + self._base_size/5, self._pos_y + self._base_size/5*4], self._dot_base_size)
        pg.draw.circle(board, "Black", [
                       self._pos_x + self._base_size/5*4, self._pos_y + self._base_size/5], self._dot_base_size)

    def paint_six(self, board):
        pg.draw.circle(board, "Black", [
                       self._pos_x + self._base_size/5, self._pos_y + self._base_size/2], self._dot_base_size)
        pg.draw.circle(board, "Black", [
                       self._pos_x + self._base_size/5*4, self._pos_y + self._base_size/2], self._dot_base_size)


class Player:
    def __init__(self, name, color):
        self._name = name
        self._color = color


class TurnManager:
    def __init__(self):
        self._turn_history = []
        self._player_on_turn = None


class Turn:
    def __init__(self, player, from_tile, to_tile):
        self._player = player
        self._from_tile = from_tile
        self._to_tile = to_tile


# Game initialization
player1 = Player("Player1", "White")
player2 = Player("Player2", "Black")
game_board = GameBoard(player1, player2)
dices = [Dice(game_board._screen_width/12*11, game_board._screen_height/2),
         Dice(game_board._screen_width/12*10, game_board._screen_height/2)]
tiles = game_board._tiles
for pos_y in range(2):
    for pos_x in range(13):
        if pos_x is 6:
            continue
        game_board._tiles.append(
            Tile(pos_x*game_board._screen_width/13 if pos_y is 0 else game_board._screen_width-(pos_x+1)*game_board._screen_width/13,
                 game_board._screen_height if pos_y is 1 else 0,
                 game_board._screen_width/13,
                 (player1._color if pos_x % 2 is 0 else player2._color) if pos_y is 0 else player1._color if pos_x % 2 is 1 else player2._color))

for column in range(5):
    tiles[0].add_stone(Stone(player1))
    tiles[6].add_stone(Stone(player2))
    tiles[17].add_stone(Stone(player1))
    tiles[23].add_stone(Stone(player2))
for column in range(3):
    tiles[4].add_stone(Stone(player2))
    tiles[19].add_stone(Stone(player1))
for column in range(2):
    tiles[11].add_stone(Stone(player1))
    tiles[12].add_stone(Stone(player2))


# General PyGame setup
pg.init()
clock = pg.time.Clock()

# Game loop
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

    for dice in dices:
        dice.paint(game_board._screen)
        dice.throw(0, 7)

    game_board.paint()
    pg.display.flip()
    clock.tick(60)
