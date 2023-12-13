import pygame
from math import sin, cos, sqrt, pi
from . import Objects
from . import Game
from . import Utils

TERRAIN_TILE_COLOR = {
    "ocean": pygame.Color(141, 158, 185, 255),
    "grassland": pygame.Color(105, 110, 54, 255),
    "desert": pygame.Color(199, 188, 157, 255),
    "plain": pygame.Color(138, 125, 65, 255),
    "jungle": pygame.Color(82, 96, 74, 255),
    "mountain": pygame.Color(68, 60, 47, 255),
}
FOOD_IMG = pygame.transform.scale(pygame.image.load('image/food.webp'), (10, 10))


def draw_regular_hexagon(screen, tile, color):
    n, r = 6, tile.radius
    x, y = tile.pos
    color = TERRAIN_TILE_COLOR.get(tile.terrain)
    #color = "black"
    if tile.tag == "path":
        color = "teal"

    _hex = pygame.draw.polygon(screen, color, [
        (x + r * sin(2 * pi * i / n), y + r * cos(2 * pi * i / n))
        for i in range(n)
    ], width=0)

    #screen.blit(FOOD_IMG, (x - tile.radius / 2, y))
    return _hex

def draw_hexagons(screen, all_tiles):
    tiles_hex_obj = {}
    for _pos, _tile in all_tiles.items():
        _hex = draw_regular_hexagon(screen, _tile, color="red")
        tiles_hex_obj[_pos] = [_tile, _hex]
    return tiles_hex_obj

def tile_hover(screen, tile):
    x, y = tile.pos
    screen.blit(FOOD_IMG, (x - tile.radius / 2, y))

def draw_units(screen, all_tiles):
    circles = {}
    for tile in all_tiles.values():
        x, y = tile.pos
        if tile.unit is not None:
            if tile.unit.selected:
                _circle = pygame.draw.circle(screen, "green", (x, y - tile.radius / 3), radius=10, width=0)
            else:
                _circle = pygame.draw.circle(screen, "black", (x, y - tile.radius / 3), radius=10, width=1)
            circles[tile.unit] = _circle
    return circles


def handle_events(unit_circles, tile_hexes):
    running = True
    ev = pygame.event.get()
    for event in ev:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            #import pdb; pdb.set_trace()
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # left click
                for _unit, _circle in unit_circles.items():
                    if _circle.collidepoint(pygame.mouse.get_pos()):
                        print(f"{_unit.owner.name} {_unit.type} clicked")
                        _unit.selected = True
                    else:
                        _unit.selected = False
            elif event.button == 3: # right click, move
                #selected_unit = Game.get_selected_unit(unit_circles)
                selected_unit = [u for u in unit_circles.keys() if u.selected == True]
                if len(selected_unit) == 0:
                    pass
                else:
                    selected_unit = selected_unit[0]
                    for _pos, _hex_list in tile_hexes.items():
                        _tile, _hex_obj = _hex_list[0], _hex_list[1]
                        if _hex_obj.collidepoint(pygame.mouse.get_pos()):
                            print(f"moving unit {selected_unit.owner.name} {selected_unit.type} from {selected_unit.pos} to {_tile.pos}")
                            #path = Utils.calc_route2(selected_unit.tile, _tile)
                            _ = Utils.calc_moves(selected_unit.moves, tile1=selected_unit.tile, tile2=_tile)
                            
                            #print(f"routed path: {path}")
                            #selected_unit.move_to(_tile)
        elif event.type == pygame.MOUSEBUTTONUP:
            for _pos, _hex_list in tile_hexes.items():
                _tile, _hex_obj = _hex_list[0], _hex_list[1]
                if _tile.tag == "path":
                    _tile.tag = None
                            

    return running


