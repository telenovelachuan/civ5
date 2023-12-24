import pygame
from core.Game import init_tiles, init_terrain, init_civilizations
from core.Graphics import draw_hexagons, draw_units, init_screen, draw_menu_bar, init_game_canvas, \
    update_unit_actions_n_avatar, draw_borders, draw_all_cities
from core.Events import handle_events
from core.Utils import get_peripheral

pygame.init()
screen = init_screen()
tiles = init_tiles(*screen.get_size())
tiles = init_terrain(tiles)
all_civs = init_civilizations(1, tiles)

draw_menu_bar(screen)

running = True
while running:
    #screen.fill("white")
    init_game_canvas(screen)
    
    
    hexes = draw_hexagons(screen, tiles)
    unit_circles = draw_units(screen, tiles)
    action_buttons = update_unit_actions_n_avatar(screen, unit_circles)
    draw_borders(screen, all_civs)
    city_banners = draw_all_cities(screen, all_civs)

    pygame.display.flip()
    running = handle_events(screen, unit_circles, tiles, hexes, action_buttons)

    
    
pygame.quit()
