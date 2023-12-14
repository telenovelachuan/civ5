import pygame
from math import sin, cos, pi

pygame.font.init()

TERRAIN_TILE_COLOR = {
    "ocean": pygame.Color(141, 158, 185, 255),
    "grassland": pygame.Color(105, 110, 54, 255),
    "desert": pygame.Color(199, 188, 157, 255),
    "plain": pygame.Color(138, 125, 65, 255),
    "jungle": pygame.Color(82, 96, 74, 255),
    "mountain": pygame.Color(68, 60, 47, 255),
}
FOOD_IMG = pygame.transform.scale(pygame.image.load('image/food.webp'), (10, 10))
FONT = pygame.font.SysFont(None, 15)
SCREEN_X = 1280
SCREEN_Y = 720



def init_screen():
    screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y))
    return screen

def draw_text(screen, text, pos):
    text = FONT.render(text, True, "black")
    screen.blit(text, pos)

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
    draw_text(screen, str(tile.seq), tile.pos)
    return _hex

def draw_hexagons(screen, all_tiles):
    hex_obj = {}
    for _seq, _tile in all_tiles.items():
        _hex = draw_regular_hexagon(screen, _tile, color="red")
        hex_obj[str(_seq)] = _hex
    return hex_obj

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


