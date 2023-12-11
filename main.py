import pygame
from core.Game import init_tiles, init_terrain
from core.Graphics import draw_hexagons

pygame.init()
screen = pygame.display.set_mode((1280, 720))
screen_size_x, screen_size_y = screen.get_size()
tiles = init_tiles(screen_size_x, screen_size_y)
tiles = init_terrain(tiles)

running = True
while running:
    screen.fill("white")
    
    
    draw_hexagons(screen, tiles)
    pygame.display.flip()

    ev = pygame.event.get()
    for event in ev:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            #import pdb; pdb.set_trace()
            running = False
    
pygame.quit()
