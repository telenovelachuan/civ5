import pygame
from math import sin, cos, sqrt, pi
from . import Objects
#from Game import init_tiles


def draw_regular_hexagon(screen, position, radius, width=1, color="black"):
    n, r = 6, radius
    x, y = position
    _hex = pygame.draw.polygon(screen, color, [
        (x + r * sin(2 * pi * i / n), y + r * cos(2 * pi * i / n))
        for i in range(n)
    ], width)
    return _hex

def draw_hexagons(screen, all_tiles):
    for _pos, _tile in all_tiles.items():
        draw_regular_hexagon(screen, _pos, _tile.radius)
