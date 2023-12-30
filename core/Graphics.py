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
# FONT = pygame.font.SysFont("applegothic", 15)
#FONT = pygame.font.Font("fonts/century_gothic.ttf", 15)
MENU_BORDER_COLOR = pygame.Color(180, 182, 158, 255)
SCREEN_X = 1280
SCREEN_Y = 720
MENU_WIDTH = 100
MENU_START_Y = SCREEN_Y - 300
TECH_CIRCLE_RADIUS = 45
TECH_CIRCLE_INTERNAL_RADIUS = TECH_CIRCLE_RADIUS * 0.95
CITY_BANNER_TRANSPARANCY = 1.5
BUTTON_COLOR = pygame.Color(20, 46, 42, 255)
TECH_CIRCLE_BG_COLOR = pygame.Color(16, 42, 37, 255)
TECH_FONT_COLOR = pygame.Color(214, 216, 175, 255)
TECH_TREE_BG_COLOR = pygame.Color(2, 2, 2, 255)
TECH_RESEARCHED_COLOR = pygame.Color(179, 145, 57, 255)
TECH_BAR_HEIGHT = 30
TECH_FRAME_BG_COLORS = {
    "researched": TECH_RESEARCHED_COLOR,
    "researching": pygame.Color(49, 87, 80, 255),
    "available": pygame.Color(77, 130, 36, 255),
    "unresearchable": TECH_TREE_BG_COLOR
}

def init_screen():
    screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y))
    return screen

def init_game_canvas(screen):
    pygame.draw.rect(screen, TERRAIN_TILE_COLOR["ocean"],
                     [MENU_WIDTH, 0, SCREEN_X - MENU_WIDTH, SCREEN_Y], width=0)

def draw_text(screen, text, pos, color="black", bold=True, size=10):
    if bold:
        _font = pygame.font.Font("fonts/gothicb.ttf", size)
    else:
        _font = pygame.font.Font("fonts/century_gothic.ttf", size)
    text = _font.render(str(text), True, color)
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
    _tech_circle = draw_tech_circle(screen, game_status["current_tech"])
    return _tech_circle


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
    pygame.draw.rect(screen, MENU_BORDER_COLOR, [pos[0], pos[1], width, height], border_radius=15, width=0)
    banner = pygame.draw.rect(screen, banner_color, [pos[0]+2, pos[1]+2, width-4, height-4], border_radius=15, width=0)
    #pygame.draw.rect(screen, banner_color, [pos[0], pos[1], width, height], border_radius=15, width=0)
    
    draw_text(screen, city.name, (pos[0] + width / 2 - len(city.name) * 2.5, pos[1] + height * 0.22), color=city.owner.color)
    draw_text(screen, city.population, (pos[0] + width * 0.1, pos[1] + height * 0.22), color=city.owner.color)
    pygame.draw.line(screen, "black", (pos[0] + width * 0.2, pos[1] + 2), (pos[0] + width * 0.2, pos[1] + height - 3), width=2)
    pygame.draw.line(screen, "black", (pos[0] + width * 0.8, pos[1] + 2), (pos[0] + width * 0.8, pos[1] + height - 3), width=2)
    return banner

def draw_all_cities(screen, all_civs):
    banners = {}
    for civ in all_civs:
        for city in civ.cities:
            _banner = draw_city_banner(screen, city)
            banners[city] = _banner
    return banners

def draw_tech_circle(screen, current_tech):
    pygame.draw.rect(screen, TECH_CIRCLE_BG_COLOR, [0, 0, MENU_WIDTH - 1, TECH_BAR_HEIGHT], border_radius=5, width=0)
    pygame.draw.rect(screen, MENU_BORDER_COLOR, [0, 0, MENU_WIDTH - 1, TECH_BAR_HEIGHT], border_radius=5, width=1)
    tech_name = current_tech.name.upper()
    draw_text(screen, tech_name, (MENU_WIDTH * 0.1, TECH_BAR_HEIGHT * 0.3), color=TECH_FONT_COLOR)
    # draw tech progress
    if current_tech.status == "researched":
        pygame.draw.circle(screen, TECH_RESEARCHED_COLOR, (50, 50 + TECH_BAR_HEIGHT), radius=TECH_CIRCLE_RADIUS, width=0)
    
    # draw tech circles
    pygame.draw.circle(screen, MENU_BORDER_COLOR, (50, 50 + TECH_BAR_HEIGHT), radius=TECH_CIRCLE_RADIUS, width=3)
    pygame.draw.circle(screen, MENU_BORDER_COLOR, (50, 50 + TECH_BAR_HEIGHT), radius=TECH_CIRCLE_RADIUS, width=3)
    tech_img = pygame.transform.scale(current_tech.image, (TECH_CIRCLE_INTERNAL_RADIUS*2, TECH_CIRCLE_INTERNAL_RADIUS*2))
    _circle = screen.blit(tech_img, (50 - TECH_CIRCLE_INTERNAL_RADIUS, 50 + TECH_BAR_HEIGHT - TECH_CIRCLE_INTERNAL_RADIUS))
    return _circle

def draw_tech_tree(screen, all_techs):
    tech_frames = {}
    pygame.draw.rect(screen, TECH_TREE_BG_COLOR, [MENU_WIDTH, 0, SCREEN_X - MENU_WIDTH, SCREEN_Y], width=0)
    valid_techs = [t for _, t in all_techs.items() if t.status in ("available", "researching")]
    start_stage = min([t.stage for t in valid_techs]) - 1
    end_stage = min([t.stage for t in valid_techs]) + 1
    techs_to_draw = [t for _, t in all_techs.items() if t.stage >= start_stage and t.stage <= end_stage]
    num_stages = end_stage - start_stage + 1
    stage_width = (SCREEN_X - MENU_WIDTH) / num_stages
    for _stage in range(start_stage, end_stage + 1):
        stage_x_start = MENU_WIDTH + _stage * stage_width
        #pygame.draw.rect(screen, "white", [stage_x_start, 0, stage_width, SCREEN_Y], width=2)
        stage_techs = {t.stage_seq:t for t in techs_to_draw if t.stage == _stage}
        num_stage_techs = len(stage_techs)
        for _stage_seq in sorted(stage_techs.keys()):
            _tech = stage_techs[_stage_seq]
            stage_tech_height = SCREEN_Y / num_stage_techs
            stage_tech_y_start = _stage_seq * stage_tech_height
            # draw tech frame
            tech_frame_width = stage_width * 0.6
            tech_frame_height = 50
            tech_frame_x = stage_x_start + stage_width / 2 - tech_frame_width / 2
            tech_frame_y = stage_tech_y_start + stage_tech_height / 2 - tech_frame_height / 2
            frame_bg_color = TECH_FRAME_BG_COLORS[_tech.status]
            pygame.draw.rect(screen, frame_bg_color, [tech_frame_x, tech_frame_y, tech_frame_width, tech_frame_height], border_radius=7, width=0)
            pygame.draw.rect(screen, MENU_BORDER_COLOR, [tech_frame_x, tech_frame_y, tech_frame_width, tech_frame_height], border_radius=7, width=2)
            # draw tech frame contents
            draw_tech_frame(screen, tech_frame_x, tech_frame_y, tech_frame_width, tech_frame_height, _tech)
            tech_frames[_tech.name.lower()] = [tech_frame_x, tech_frame_y, tech_frame_width, tech_frame_height]
    
    # draw tech frame relations
    for _tech in techs_to_draw:
        _tech_frame = tech_frames[_tech.name.lower()]
        end_point_x = _tech_frame[0]
        end_point_y = _tech_frame[1] + _tech_frame[3] / 2
        for _dep in _tech.dependencies:
            _dep_frame = tech_frames[_dep.name.lower()]
            start_point_x = _dep_frame[0] + _dep_frame[2]
            start_point_y = _dep_frame[1] + _dep_frame[3] / 2
            pygame.draw.line(screen, MENU_BORDER_COLOR, (start_point_x, start_point_y), (end_point_x, end_point_y), width=3)

    # back button
    button_width = SCREEN_X * 0.07
    button_height = SCREEN_Y * 0.05
    pygame.draw.rect(screen, BUTTON_COLOR, [MENU_WIDTH + SCREEN_X * 0.01, SCREEN_Y - button_height, button_width, button_height], border_radius=7, width=0)
    button_return = pygame.draw.rect(screen, MENU_BORDER_COLOR, [MENU_WIDTH + SCREEN_X * 0.01, SCREEN_Y - button_height, button_width, button_height], border_radius=7, width=2)
    draw_text(screen, "BACK", (MENU_WIDTH + SCREEN_X * 0.01 + button_width * 0.28, SCREEN_Y - button_height + button_height * 0.2), MENU_BORDER_COLOR, bold=False, size=15)
    return button_return

def draw_tech_frame(screen, frame_x, frame_y, frame_width, frame_height, tech):
    # tech circle
    tech_radius = frame_height * 0.8 / 2
    circle_center = (frame_x + frame_width*0.05 + tech_radius, frame_y + frame_height*0.1 + tech_radius)
    pygame.draw.circle(screen, MENU_BORDER_COLOR, circle_center, radius=tech_radius, width=0)
    pygame.draw.circle(screen, "black", circle_center, radius=tech_radius*0.85, width=1)
    img_radius = tech_radius*0.85 - 1
    _tech_img = pygame.transform.scale(tech.image, (img_radius * 2, img_radius * 2))
    screen.blit(_tech_img, (circle_center[0] - img_radius, circle_center[1] - img_radius))
    # tech name
    draw_text(screen, tech.name, (frame_x + frame_width * 0.25, frame_y + frame_height * 0.04),
              color=MENU_BORDER_COLOR, size=14)
    # icons
    icon_radius = img_radius * 0.8
    for idx, icon in enumerate(tech.icons):
        icon_img = pygame.transform.scale(icon, (icon_radius * 2, icon_radius * 2))
        icon_x = frame_x + frame_width * 0.25 + idx * frame_width * 0.12
        screen.blit(icon_img, (icon_x, frame_y + frame_height * 0.4))
    
def draw_city(screen):
    pygame.draw.rect(screen, "black", [MENU_WIDTH, 0, SCREEN_X - MENU_WIDTH, SCREEN_Y], width=0)