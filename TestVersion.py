# Imports
import pygame as pg
import random
import sys

import ctypes


# Classes


class Player:
    def __init__(self, name: str, color: pg.color):
        self.name = name
        self.color = color


class ClickManager:
    def __init__(self):
        pass

    def click(self, x: int, y: int):
        pass


class Stone:
    white_color = (255, 255, 255)
    black_color = (0, 0, 0)
    highlight_color = (255, 0, 0)
    highlight_thickness = 5
    base_radius = 40
    circle_collider = None
    def __init__(self, player: Player):
        self.highlighted = False
        self.player = player

    def paint(self, screen: pg.surface, pos_x: float, pos_y: float, num: int, pos_x_shift: float, direction: bool):
        y_shifted = (pos_y + (2*self.base_radius)*(num)+self.base_radius) if direction else (
            pos_y + (2*self.base_radius)*(-num)-self.base_radius)
        color = self.white_color if self.player.color is "White" else self.black_color
        self.circle_collider = pg.draw.circle(screen, color, (pos_x + pos_x_shift,
                       y_shifted), self.base_radius)
        
        
        if self.highlighted:
            pg.draw.circle(screen, self.highlight_color, (pos_x + pos_x_shift,
                                                          y_shifted), self.base_radius, self.highlight_thickness)


class Tile:
    white_color = (133, 78, 35)
    black_color = (107, 74, 53)
    highlight_color = (255, 0, 0)
    highlight_thickness = 5
    height_multiplier = 3

    def __init__(self, pos_x: float, pos_y: float, size: float, color: pg.Color):
        self.highlighted = False
        self.stones = []
        self._size = size
        self._color = color
        self._pos_x = pos_x
        self._pos_y = pos_y

    def add_stone(self, stone: Stone):
        self.stones.append(stone)

    def remove_stone(self):
        self.stones[-1].remove()

    def paint(self, screen):
        tileDirection = self._size*self.height_multiplier if self._pos_y is 0 else - \
            self._size*self.height_multiplier
        points = [[self._pos_x, self._pos_y],
                  [self._pos_x + self._size / 2, self._pos_y + tileDirection],
                  [self._pos_x + self._size, self._pos_y]]

        pg.draw.polygon(
            screen, self.white_color if self._color is "White" else self.black_color, points)
        if self.highlighted:
            pg.draw.polygon(
                screen, self.highlight_color, points, self.highlight_thickness)

        for num in range(len(self.stones)):
            self.stones[num].paint(screen, self._pos_x,
                                   self._pos_y, num, self._size/2, True if self._pos_y is 0 else False)

    def highlight_stone(self):
        if len(self.stones) > 0:
            self.stones[-1].highlighted = True

    def unhighlight_stones(self):
        for stone in self.stones:
            stone.highlighted = False


class GameBoard:
    screen_width = 1600
    screen_height = 1000
    base_margin = 30
    box_color = (171, 117, 46)
    surface_color = (247, 236, 200)

    def __init__(self, player1: Player, player2: Player):
        self.tiles = []
        self.players = [player1, player2]
        self._turn_manager = TurnManager()
        self._screen = pg.display.set_mode(
            (self.screen_width, self.screen_height))
        self._screen.fill(self.box_color)

    def paint(self):
        for tile in self.tiles:
            tile.paint(self._screen)

    def move_stone(self, tile_from: Tile, tile_to: Tile):
        tile_to.add_stone(tile_from.stones[-1])
        tile_from.remove_stone()


class Dice:
    base_size = 100
    dot_base_size = 10
    border_radius = 15

    def __init__(self, pos_x: float, pos_y: float):
        self._number = 1
        self._pos_x = pos_x-self.base_size/2
        self._pos_y = pos_y-self.base_size/2

    def throw(self, rand_from: int, rand_to: int):
        self._number = random.randint(rand_from, rand_to)

    def paint(self, screen: pg.surface):
        pg.draw.rect(screen, "White", [
                     self._pos_x, self._pos_y, self.base_size, self.base_size], 0, self.border_radius)
        match self._number:
            case 1:
                self.paint_one(screen)
            case 2:
                self.paint_two(screen)
            case 3:
                self.paint_one(screen)
                self.paint_two(screen)
            case 4:
                self.paint_two(screen)
                self.paint_four(screen)
            case 5:
                self.paint_one(screen)
                self.paint_two(screen)
                self.paint_four(screen)
            case 6:
                self.paint_four(screen)
                self.paint_two(screen)
                self.paint_six(screen)

    def paint_one(self, screen: pg.surface):
        pg.draw.circle(screen, "Black", [
                       self._pos_x + self.base_size/2, self._pos_y + self.base_size/2], self.dot_base_size)

    def paint_two(self, screen: pg.surface):
        pg.draw.circle(screen, "Black", [
                       self._pos_x + self.base_size/5, self._pos_y + self.base_size/5], self.dot_base_size)
        pg.draw.circle(screen, "Black", [
                       self._pos_x + self.base_size/5*4, self._pos_y + self.base_size/5*4], self.dot_base_size)

    def paint_four(self, screen: pg.surface):
        pg.draw.circle(screen, "Black", [
                       self._pos_x + self.base_size/5, self._pos_y + self.base_size/5*4], self.dot_base_size)
        pg.draw.circle(screen, "Black", [
                       self._pos_x + self.base_size/5*4, self._pos_y + self.base_size/5], self.dot_base_size)

    def paint_six(self, screen: pg.surface):
        pg.draw.circle(screen, "Black", [
                       self._pos_x + self.base_size/5, self._pos_y + self.base_size/2], self.dot_base_size)
        pg.draw.circle(screen, "Black", [
                       self._pos_x + self.base_size/5*4, self._pos_y + self.base_size/2], self.dot_base_size)


class TurnManager:
    possible_turns = []

    def __init__(self):
        self._turn_history = []
        self._player_on_turn = None


class Turn:
    def __init__(self, player: Player, from_tile: Tile, to_tile: Tile):
        self._player = player
        self._from_tile = from_tile
        self._to_tile = to_tile


# Game initialization
player1 = Player("Player1", "White")
player2 = Player("Player2", "Black")
click_manager = ClickManager()
game_board = GameBoard(player1, player2)
dices = [Dice(game_board.screen_width/12*11, game_board.screen_height/2),
         Dice(game_board.screen_width/12*10, game_board.screen_height/2)]
tiles = game_board.tiles
for pos_y in range(2):
    for pos_x in range(13):
        if pos_x is 6:
            continue
        game_board.tiles.append(
            Tile(pos_x*game_board.screen_width/13 if pos_y is 1 else game_board.screen_width-(pos_x+1)*game_board.screen_width/13,
                 game_board.screen_height if pos_y is 1 else 0, game_board.screen_width/13,
                 (player1.color if pos_x % 2 is 0 else player2.color) if pos_y is 1 else player1.color if pos_x % 2 is 1 else player2.color))

for column in range(5):
    tiles[11].add_stone(Stone(player1))
    tiles[12].add_stone(Stone(player2))
    tiles[18].add_stone(Stone(player1))
    tiles[5].add_stone(Stone(player2))
for column in range(3):
    tiles[16].add_stone(Stone(player1))
    tiles[7].add_stone(Stone(player2))
for column in range(2):
    tiles[0].add_stone(Stone(player1))
    tiles[23].add_stone(Stone(player2))


# General PyGame setup
pg.init()
clock = pg.time.Clock()

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

        # handle MOUSEBUTTONUP
        if event.type == pg.MOUSEBUTTONUP:
            pos = pg.mouse.get_pos()
            for tile in tiles:
                for stone in tile.stones:
                    if(stone.circle_collider.collidepoint(pos)):
                        #HERE COLLIZION DETECTION
                        print(stone)
                    
            
    
# Game loop
    for dice in dices:
        dice.paint(game_board._screen)
        dice.throw(0, 7)
    game_board.paint()

# PyGame Code
    pg.display.flip()
    clock.tick(60)
