# Imports
import pygame as pg
import pygame.gfxdraw as gfxdraw
import sys

# Functions
def draw_half(board):
    count = 6
    for i in range(6):
        width = board.get_width()
        height = board.get_height()
        gfxdraw.filled_polygon(board, [[i*width/count, 0], [(i+1)*width/count-(width/count/2), height/2-height/12], [(i+1)*width/count, 0]], triangle_colors[1] if i%2 == 0 else triangle_colors[0])
        gfxdraw.filled_polygon(board, [[i*width/count, height], [(i+1)*width/count-(width/count/2), height/2+height/12], [(i+1)*width/count, height]], triangle_colors[1] if i%2 == 0 else triangle_colors[0])

# Variables
triangle_colors = ((133, 78, 35),(107, 74, 53))
box_color = (171,117,46)
surface_color = (247, 236, 200)
screen_width, screen_height = 1400,850
base_margin = 30

# General setup
pg.init()
clock = pg.time.Clock()

# Display setup
screen = pg.display.set_mode((screen_width, screen_height))
screen.fill(box_color) 
gameboard = (pg.Surface((600, 800)),pg.Surface((600, 800)))
gameboard[0].fill(surface_color)
gameboard[1].fill(surface_color)



# Game loop
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

    pg.display.flip()
    clock.tick(60)

# Drawing the board
    screen.blit(gameboard[0], (base_margin, base_margin))
    screen.blit(gameboard[1], (screen_width/2+2*base_margin, base_margin))    
    draw_half(gameboard[0])
    draw_half(gameboard[1])

    




    

    
