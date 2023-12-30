import pygame
from core.Game import init_tiles, init_terrain, init_civilizations, game_status
from core.Graphics import draw_hexagons, draw_units, init_screen, draw_menu_bar, init_game_canvas, \
    update_unit_actions_n_avatar, draw_borders, draw_all_cities, draw_tech_tree, draw_city
from core.Events import handle_normal_events, handle_tech_events, handle_city_events

pygame.init()
screen = init_screen()
tiles = init_tiles(*screen.get_size())
tiles = init_terrain(tiles)
all_civs = init_civilizations(1, tiles)
all_techs = game_status["tech_tree"]
tech_circle = draw_menu_bar(screen, game_status)
drawing_mode = "normal"

running = True
while running:
    #screen.fill("white")
    init_game_canvas(screen)
    
    if drawing_mode == "normal":
        hexes = draw_hexagons(screen, tiles)
        unit_circles = draw_units(screen, tiles)
        action_buttons = update_unit_actions_n_avatar(screen, unit_circles)
        draw_borders(screen, all_civs)
        city_banners = draw_all_cities(screen, all_civs)

        pygame.display.flip()
        results_dict = handle_normal_events(screen, unit_circles, tiles, hexes, action_buttons, tech_circle, city_banners)
    elif drawing_mode == "tech":
        btn_return = draw_tech_tree(screen, all_techs)
        pygame.display.flip()
        results_dict = handle_tech_events(btn_return)
    elif drawing_mode == "city":
        draw_city(screen)
        pygame.display.flip()
        results_dict = handle_city_events(tech_circle)
    
    running = results_dict["running"]
    drawing_mode = results_dict["drawing_mode"]
    
    
pygame.quit()
