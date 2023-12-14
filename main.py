import pygame
from core.Game import init_tiles, init_terrain, init_civilizations
from core.Graphics import draw_hexagons, draw_units, init_screen
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

    # # hover over tiles
    # for _pos, _hex_list in hexes.items():
    #     _tile, _hex_obj = _hex_list[0], _hex_list[1]
    #     if _hex_obj.collidepoint(pygame.mouse.get_pos()):
    #         tile_hover(screen, _tile)

    pygame.display.flip()
    running = handle_events(screen, unit_circles, tiles, hexes)

    
pygame.quit()
