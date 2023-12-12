import pygame
from math import sin, cos, sqrt, pi
from . import Objects

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

