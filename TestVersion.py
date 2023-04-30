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
        self.screen = pg.display.set_mode(
            (self._screen_width, self._screen_height))
        self.screen.fill(self._box_color)

    def paint(self):
        for tile in self._tiles:
            tile.paint(self.screen)

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
    def __init__(self, color):
        self._white_color = (255, 255, 255)
        self._black_color = (0, 0, 0)
        self._color = color
        self._base_radius = 40

    def paint(self, board, pos_x, pos_y, num, pos_x_shift, direction):
        y_shifted = (pos_y + (2*self._base_radius)*(num)+self._base_radius) if direction else (
            pos_y + (2*self._base_radius)*(-num)-self._base_radius)
        color = self._white_color if self._color is "White" else self._black_color
        pg.draw.circle(board, color, (pos_x + pos_x_shift,
                       y_shifted), self._base_radius)


class Dice:
    def __init__(self):
        self._random_number = None

    def throw(self, rand_from, rand_to):
        self._random_number = random.randint(rand_from, rand_to)


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
for pos_y in range(2):
    for pos_x in range(13):
        if pos_x is 6:
            continue
        game_board._tiles.append(
            Tile(pos_x*game_board._screen_width/13,
                 game_board._screen_height if pos_y is 1 else 0,
                 game_board._screen_width/13,
                 (player1._color if pos_x % 2 is 0 else player2._color) if pos_y is 0 else player1._color if pos_x % 2 is 1 else player2._color))
for columns in range(0, 19, 6):
    for rows in range(5):
        game_board._tiles[columns].add_stone(
            Stone(player2._color if columns % 18 is 0 else player1._color))

for rows in range(3):
    game_board._tiles[5].add_stone(
        Stone(player2._color))
    game_board._tiles[17].add_stone(
        Stone(player1._color))

for rows in range(2):
    game_board._tiles[11].add_stone(
        Stone(player1._color))
    game_board._tiles[23].add_stone(
        Stone(player2._color))

# General PyGame setup
pg.init()
clock = pg.time.Clock()

# Game loop
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

    game_board.paint()
    pg.display.flip()
    clock.tick(60)
