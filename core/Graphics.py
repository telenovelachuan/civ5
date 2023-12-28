import pygame, os
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
IMG_DICT = {
    "food": pygame.transform.scale(pygame.image.load('image/food.webp'), (10, 10)),
    "do_nothing": pygame.transform.scale(pygame.image.load('image/do_nothing.png'), (30, 30)),
    "sleep": pygame.transform.scale(pygame.image.load('image/sleep.png'), (30, 30)),
    "settle": pygame.transform.scale(pygame.image.load('image/settle.png'), (30, 30))
}
FONT = pygame.font.SysFont(None, 15)
MENU_BORDER_COLOR = pygame.Color(180, 182, 158, 255)
SCREEN_X = 1280
SCREEN_Y = 720
MENU_WIDTH = 100
MENU_START_Y = SCREEN_Y - 300
TECH_CIRCLE_RADIUS = 45
TECH_CIRCLE_INTERNAL_RADIUS = TECH_CIRCLE_RADIUS * 0.95
CITY_BANNER_TRANSPARANCY = 1.5
TECH_BG_COLOR = pygame.Color(16, 42, 37, 255)
TECH_FONT_COLOR = pygame.Color(214, 216, 175, 255)
TECH_COMPLETED_COLOR = pygame.Color(179, 145, 57, 255)
TECH_BAR_HEIGHT = 30

def load_tech_images():
    results = {}
    for _name in os.listdir("image/techs"):
        if _name.endswith(".webp"):
            results[_name.split(".")[0].lower()] = pygame.transform.scale(pygame.image.load(f'image/techs/{_name}'),
                                                        (TECH_CIRCLE_INTERNAL_RADIUS*2, TECH_CIRCLE_INTERNAL_RADIUS*2))
    return results

TECH_IMAGES = load_tech_images()

def init_screen():
    screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y))
    return screen

def init_game_canvas(screen):
    pygame.draw.rect(screen, TERRAIN_TILE_COLOR["ocean"],
                     [MENU_WIDTH, 0, SCREEN_X - MENU_WIDTH, SCREEN_Y], width=0)

def draw_text(screen, text, pos, color="black"):
    text = FONT.render(str(text), True, color)
    screen.blit(text, pos)

def draw_regular_hexagon(screen, tile, color):
    n, r = 6, tile.radius
    x, y = tile.pos
    color = TERRAIN_TILE_COLOR.get(tile.terrain)
    #color = "black"
    if tile.tag == "path":
        color = "teal"
    elif tile.tag == "dragged":
        color = "cyan3"

    _hex = pygame.draw.polygon(screen, color, [
        (x + r * sin(2 * pi * i / n), y + r * cos(2 * pi * i / n))
        for i in range(n)
    ], width=0)

    #screen.blit(FOOD_IMG, (x - tile.radius / 2, y))
    draw_text(screen, str(tile.seq), (tile.pos[0] - tile.radius / 2, tile.pos[1] - tile.radius / 2))
    return _hex

def draw_hexagons(screen, all_tiles):
    hex_obj = {}
    for _seq, _tile in all_tiles.items():
        _hex = draw_regular_hexagon(screen, _tile, color="red")
        hex_obj[_seq] = _hex
    return hex_obj

# def tile_hover(screen, tile):
#     x, y = tile.pos
#     screen.blit(FOOD_IMG, (x - tile.radius / 2, y))

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

def draw_menu_bar(screen, game_status):
    screen_x, screen_y = screen.get_size()
    pygame.draw.rect(screen, "white", pygame.Rect(0, 0, MENU_WIDTH - 1, screen_y), width=0)
    pygame.draw.rect(screen, MENU_BORDER_COLOR, [0, 0, MENU_WIDTH - 1, screen_y], width=3)
    draw_tech_circle(screen, game_status["current_tech"])


def update_unit_actions_n_avatar(screen, unit_circles):
    # clear out previous draws
    pygame.draw.rect(screen, "white", [0, MENU_START_Y, 50, 150], width=0)
    for _unit in unit_circles.keys():
        if _unit.selected:
            return draw_action_box(screen, _unit)
    return None


def draw_action_box(screen, selected_unit):
    # screen_x, screen_y = screen.get_size()
    pygame.draw.rect(screen, "black", [0, MENU_START_Y, 50, 150], width=0)
    actions = selected_unit.actions
    results = {}
    for idx, _action in enumerate(actions):
        _img = IMG_DICT[_action]
        _button = screen.blit(_img, (10, MENU_START_Y + (10 + 30) * idx))
        results[_action] = _button

    return results

def draw_borders(screen, all_civs):
    for civ in all_civs:
        _borders = civ.borders
        for _border in _borders:
            pygame.draw.line(screen, civ.color, _border[0], _border[1], width=3)

def lighten_color(color, pct=0.1):
    new_r = int(255 - (255 - color.r) * 0.2)
    new_g = int(255 - (255 - color.g) * 0.2)
    new_b = int(255 - (255 - color.b) * 0.2)
    return pygame.Color(new_r, new_g, new_b, 255)

def draw_city_banner(screen, city):
    city_pos = city.tile.pos
    width = city.tile.radius * 4
    height = city.tile.radius * 0.8
    pos = (city_pos[0] - width / 2, city_pos[1] - city.tile.radius * 1 - height)
    banner_color = lighten_color(city.owner.color)
    banner = pygame.draw.rect(screen, banner_color, [pos[0], pos[1], width, height], border_radius=15, width=0)
    pygame.draw.rect(screen, "black", [pos[0], pos[1], width, height], border_radius=15, width=1)
    draw_text(screen, city.name, (pos[0] + width / 2 - len(city.name) * 2.5, pos[1] + height * 0.3), color=city.owner.color)
    draw_text(screen, city.population, (pos[0] + width * 0.1, pos[1] + height * 0.3), color=city.owner.color)
    pygame.draw.line(screen, "black", (pos[0] + width * 0.2, pos[1]), (pos[0] + width * 0.2, pos[1] + height - 1), width=2)
    pygame.draw.line(screen, "black", (pos[0] + width * 0.8, pos[1]), (pos[0] + width * 0.8, pos[1] + height - 1), width=2)
    return banner

def draw_all_cities(screen, all_civs):
    banners = []
    for civ in all_civs:
        for city in civ.cities:
            _banner = draw_city_banner(screen, city)
            banners.append(_banner)
    return banners

def draw_tech_circle(screen, current_tech):
    pygame.draw.rect(screen, TECH_BG_COLOR, [0, 0, MENU_WIDTH - 1, TECH_BAR_HEIGHT], border_radius=5, width=0)
    pygame.draw.rect(screen, MENU_BORDER_COLOR, [0, 0, MENU_WIDTH - 1, TECH_BAR_HEIGHT], border_radius=5, width=1)
    tech_name = current_tech[0].upper()
    draw_text(screen, tech_name, (MENU_WIDTH * 0.1, TECH_BAR_HEIGHT * 0.3), color=TECH_FONT_COLOR)
    # draw tech progress
    finished, total = current_tech[1], current_tech[2]
    if finished >= total:
        pygame.draw.circle(screen, TECH_COMPLETED_COLOR, (50, 50 + TECH_BAR_HEIGHT), radius=TECH_CIRCLE_RADIUS, width=0)
    
    # draw tech circles
    pygame.draw.circle(screen, MENU_BORDER_COLOR, (50, 50 + TECH_BAR_HEIGHT), radius=TECH_CIRCLE_RADIUS, width=3)
    pygame.draw.circle(screen, MENU_BORDER_COLOR, (50, 50 + TECH_BAR_HEIGHT), radius=TECH_CIRCLE_RADIUS, width=3)
    tech_img = TECH_IMAGES[tech_name.lower()]
    screen.blit(tech_img, (50 - TECH_CIRCLE_INTERNAL_RADIUS, 50 + TECH_BAR_HEIGHT - TECH_CIRCLE_INTERNAL_RADIUS))