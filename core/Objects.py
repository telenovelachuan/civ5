import random

TILE_RADIUS = 30

class Tile():
    def __init__(self, center_pos):
        self.pos = center_pos
        self.radius = TILE_RADIUS
        self.left = None
        self.right = None
        self.left_up = None
        self.right_up = None
        self.left_down = None
        self.right_down = None
        self.terrain = None
        self.unit = None
        self.tag = None
    
    @property
    def neighbors(self):
        neighbors = [self.left, self.left_up, self.right_up, self.right, self.right_down, self.left_down]
        return [t for t in neighbors if t is not None]
    
    @property
    def food(self):
        if self.terrain in ["grassland", "ocean"]:
            return 2
        elif self.terrain == "plain":
            return 1
        else:
            return 0
        
    @property
    def move_consumption(self):
        if self.terrain in ["jungle", "hill"]:
             return 2
        else:
            return 1
        
    @property
    def production(self):
        if self.terrain == "hill":
            return 2
        elif self.terrain == "plain":
            return 1
        return 0


class Civilization():
    def __init__(self, civ_name, all_tiles):
        self.name = civ_name
        self.units = []
        # init settler
        valid_tiles = [t for t in all_tiles.values() if t.terrain not in ["ocean", "mountain"] and t.unit is None]
        settler_tile = random.choice(valid_tiles)
        settler = Unit("settler", settler_tile, self)
        settler_tile.unit = settler


class Unit():
    def __init__(self, unit_type, tile, owner):
        self.type = unit_type
        self.tile = tile
        self.owner = owner
        self.pos = self.tile.pos
        self.selected = False
        self.moves = 2

    def move_to(self, new_tile):
        self.pos = new_tile.pos
        self.tile.unit = None
        self.tile = new_tile
        self.tile.unit = self
