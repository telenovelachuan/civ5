import pygame
from core.Game import init_tiles, init_terrain
from core.Graphics import draw_hexagons, tile_hover

pygame.init()
screen = pygame.display.set_mode((1280, 720))
screen_size_x, screen_size_y = screen.get_size()
tiles = init_tiles(screen_size_x, screen_size_y)
tiles = init_terrain(tiles)


running = True
while running:
    screen.fill("white")
    
    
    hexes = draw_hexagons(screen, tiles)

    # # hover over tiles
    # for _pos, _hex_list in hexes.items():
    #     _tile, _hex_obj = _hex_list[0], _hex_list[1]
    #     if _hex_obj.collidepoint(pygame.mouse.get_pos()):
    #         tile_hover(screen, _tile)

    pygame.display.flip()

    ev = pygame.event.get()
    for event in ev:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            #import pdb; pdb.set_trace()
            running = False
    
pygame.quit()
