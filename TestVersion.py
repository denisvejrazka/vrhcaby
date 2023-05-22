# Imports
import pygame as pg
import random
import sys
import tkinter as tk
import os


window = tk.Tk()



# create a menubar
menubar = tk.Menu(window)
window.config(menu=menubar)

# create the file_menu
file_menu = tk.Menu(
    menubar,
    tearoff=0
)

# add menu items to the File menu
file_menu.add_command(label='Save')
file_menu.add_command(label='Load')
file_menu.add_command(label='Close')
file_menu.add_separator()

# add Exit menu item
file_menu.add_command(
    label='Exit',
    command=window.destroy
)

# add the File menu to the menubar
menubar.add_cascade(
    label="File",
    menu=file_menu
)
# create the Help menu
help_menu = tk.Menu(
    menubar,
    tearoff=0
)

help_menu.add_command(label='Welcome')
help_menu.add_command(label='About...')

# add the Help menu to the menubar
menubar.add_cascade(
    label="Help",
    menu=help_menu
)

embed = tk.Frame(window, width=1600, height=1000)
window.resizable(False,False)
embed.pack()

# Tell pygame's SDL window which window ID to use
os.environ['SDL_WINDOWID'] = str(embed.winfo_id())
# Show the window so it's assigned an ID.
window.update()



# Classes



class Player:
    def __init__(self, name: str, color: pg.color):
        self.name = name
        self.color = color


class ClickManager:

    def __init__(self):
        self.currentTile = None

    def click(self, tiles, dices, turn_manager, position):
        for tile in tiles:
            if tile.highlighted and tile.tile_collider.collidepoint(position):
                for tile2 in tiles:
                    tile2.unhighlight_stones()
                    tile2.highlighted = False
                #POKUD TU JE JEDEN KÁMEN PAK HO VYHOĎ
                GameBoard.move_stone(self.currentTile, tile)
                turn_manager.player_on_turn = player1 if turn_manager.player_on_turn == player2 else player2
                return
        for tile in tiles:
            for stone in tile.stones:
                if stone.highlighted and stone.circle_collider.collidepoint(position):
                    self.currentTile = tile
                    for tile2 in tiles:
                        if tile != tile2:
                            tile2.unhighlight_stones()
                    turn_manager.find_available_turns(dices, tiles, tile)
                    return
        for tile in tiles:
            tile.unhighlight_stones()
            tile.highlighted = False
        self.currentTile = None
        turn_manager.find_all_stones(game_board.tiles)


class Stone:
    white_color = (255, 255, 255)
    black_color = (0, 0, 0)
    highlight_color = (255, 0, 0)
    highlight_thickness = 5
    base_radius = 40

    def __init__(self, player: Player):
        self.circle_collider = None
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
        self.tile_collider = None
        self.highlighted = False
        self.stones = []
        self._size = size
        self._color = color
        self._pos_x = pos_x
        self._pos_y = pos_y

    def add_stone(self, stone: Stone):
        self.stones.append(stone)

    def remove_stone(self):
        self.stones.pop()

    def paint(self, screen):
        tileDirection = self._size*self.height_multiplier if self._pos_y is 0 else - \
            self._size*self.height_multiplier
        points = [[self._pos_x, self._pos_y],
                  [self._pos_x + self._size / 2, self._pos_y + tileDirection],
                  [self._pos_x + self._size, self._pos_y]]

        self.tile_collider = pg.draw.polygon(
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
        self.game_over = False
        self.home = Home()

    def paint(self):
        for tile in self.tiles:
            tile.paint(self._screen)

    @staticmethod
    def move_stone(self, tile_from: Tile, tile_to: Tile):
        tile_to.add_stone(tile_from.stones[-1])
        tile_from.remove_stone()
        home_index = self.tiles.index(tile_to)
        self.home.set_tile(home_index, tile_to)


class Dice:
    roll_used = False
    base_size = 100
    dot_base_size = 10
    border_radius = 15
    color_available = (240, 240, 240)
    color_disabled = (125, 125, 125)

    def __init__(self, pos_x: float, pos_y: float):
        self.value = 1
        self._pos_x = pos_x-self.base_size/2
        self._pos_y = pos_y-self.base_size/2

    def throw(self, rand_from: int, rand_to: int):
        self.roll_used = False
        self.value = random.randint(rand_from, rand_to)

    def paint(self, screen: pg.surface):
        if self.roll_used:
            pg.draw.rect(screen, self.color_disabled, [
                self._pos_x, self._pos_y, self.base_size, self.base_size], 0, self.border_radius)
        else:
            pg.draw.rect(screen, self.color_available, [
                self._pos_x, self._pos_y, self.base_size, self.base_size], 0, self.border_radius)
        match self.value:
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
    available_turns = []
    player_changed = True

    def __init__(self):
        self._turn_history = []
        self._player_on_turn = None

    @property
    def player_on_turn(self):
        return self._player_on_turn

    @player_on_turn.setter
    def player_on_turn(self, value):
        self._player_on_turn = value
        self.player_changed = True

    def find_all_stones(self, tiles):
        for tile in tiles:
            if len(tile.stones) > 0:
                if tile.stones[0].player == self.player_on_turn:
                    tile.highlight_stone()

    def find_available_turns(self, dices, tiles, tile):
        tile_index = tiles.index(tile)
        for dice in dices:
            if tile_index - dice.value > 0 and self.player_on_turn == player1:
                self.find_available_turn(tiles, tile_index-dice.value)
            if tile_index + dice.value < 24 and self.player_on_turn == player2:
                self.find_available_turn(tiles, tile_index+dice.value)

    def find_available_turn(self, tiles, tile_index):
        if len(tiles[tile_index].stones) == 1:
            tiles[tile_index].highlighted = True
        if len(tiles[tile_index].stones) == 0:
            tiles[tile_index].highlighted = True
        if len(tiles[tile_index].stones) > 0:
            if tiles[tile_index].stones[0].player == self._player_on_turn:
                tiles[tile_index].highlighted = True

class Home:

    def __init__(self, stones: list[Tile]):
        self.tiles = tiles
        game_board = GameBoard()

    def set_tile(self, index, tile):
        self.tiles[index] = tile
        self.check_win_condition()

    def check_win_condition(self):
        #zjištění, zda jsou všechny kameny v domovském prostoru hráče 1 nebo 2 buď prázný nebo mají správně nastaveného hráče.
        player1_home = all(len(tile.stones) == 0 or tile.stones[0].player == player1 for tile in self.tiles[:6])
        player2_home = all(len(tile.stones) == 0 or tile.stones[0].player == player2 for tile in self.tiles[18:])
        
        if player1_home:
            self.winner = 1
        elif player2_home:
            self.winner = 2

        if self.winner is not None:
            game_board.game_over = True



# Game initialization
player1 = Player("Player1", "White")
player2 = Player("Player2", "Black")
click_manager = ClickManager()
game_board = GameBoard(player1, player2)
turn_manager = TurnManager()
turn_manager.player_on_turn = player1
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

running = True
def done():
    global running
    running = False

window.protocol("WM_DELETE_WINDOW", done)


clock = pg.time.Clock()

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            os._exit(1)
            pg.quit()
            sys.exit()
            

        # handle MOUSEBUTTONUP
        if event.type == pg.MOUSEBUTTONUP:
            click_manager.click(tiles, dices, turn_manager, pg.mouse.get_pos())
        
        if game_board.game_over:
            #UI pro výhru a prohru
            pass
                    
            
    
# Game loop
    for dice in dices:
        dice.paint(game_board._screen)
    game_board.paint()

    if turn_manager.player_changed:
        turn_manager.player_changed = False
        for dice in dices:
            dice.throw(1, 6)
        turn_manager.find_all_stones(game_board.tiles)
        
# PyGame Code
    pg.display.flip()
    window.update_idletasks()
    window.update()
    clock.tick(60)
    game_board._screen.fill(game_board.box_color)





