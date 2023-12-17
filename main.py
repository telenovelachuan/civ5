import pygame
from core.Game import init_tiles, init_terrain, init_civilizations
from core.Graphics import draw_hexagons, draw_units, init_screen, draw_menu_bar
from core.Events import handle_events
from core.Utils import get_peripheral

pygame.init()
screen = init_screen()
tiles = init_tiles(*screen.get_size())
tiles = init_terrain(tiles)
init_civilizations(1, tiles)

running = True
while running:
    screen.fill("white")
    
    
    hexes = draw_hexagons(screen, tiles)
    unit_circles = draw_units(screen, tiles)
    draw_menu_bar(screen)

    pygame.display.flip()
    running = handle_events(screen, unit_circles, tiles, hexes)

    
    
pygame.quit()
