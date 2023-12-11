import pygame
from math import sin, cos, sqrt, pi
from . import Objects

TERRAIN_TILE_COLOR = {
    "ocean": pygame.Color(141, 158, 185, 255),
    "grassland": pygame.Color(105, 110, 54, 255),
}


def draw_regular_hexagon(screen, tile, color):
    n, r = 6, tile.radius
    x, y = tile.pos
    color = TERRAIN_TILE_COLOR.get(tile.terrain)
    #color = "black"
    _hex = pygame.draw.polygon(screen, color, [
        (x + r * sin(2 * pi * i / n), y + r * cos(2 * pi * i / n))
        for i in range(n)
    ], width=0)
    return _hex

def draw_hexagons(screen, all_tiles):
    for _pos, _tile in all_tiles.items():
        draw_regular_hexagon(screen, _tile,color="red")

