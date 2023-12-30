import random
import math
import pygame

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
        self.seq = None
        self.owner = None
        self.city = None
        self.vertexes = {
            "left_up": (round(self.pos[0] - self.radius / 2 * math.sqrt(3), 2), self.pos[1] - self.radius / 2),
            "up": (self.pos[0], self.pos[1] - self.radius),
            "right_up": (round(self.pos[0] + self.radius / 2 * math.sqrt(3), 2), self.pos[1] - self.radius / 2),
            "right_down": (round(self.pos[0] + self.radius / 2 * math.sqrt(3), 2), self.pos[1] + self.radius / 2),
            "down": (self.pos[0], self.pos[1] + self.radius),
            "left_down": (round(self.pos[0] - self.radius / 2 * math.sqrt(3), 2), self.pos[1] + self.radius / 2),
        }

        # self.edges = {
        #     self.left_up: [self.vertexes["left_up"], self.vertexes["up"]],
        #     self.right_up: [self.vertexes["up"], self.vertexes["right_up"]],
        #     self.right: [self.vertexes["right_up"], self.vertexes["right_down"]],
        #     self.right_down: [self.vertexes["right_down"], self.vertexes["down"]],
        #     self.left_down: [self.vertexes["down"], self.vertexes["left_down"]],
        #     self.left: [self.vertexes["left_down"], self.vertexes["left_up"]]
        # }

    @property
    def edges(self):
        return {
            self.left_up: [self.vertexes["left_up"], self.vertexes["up"]],
            self.right_up: [self.vertexes["up"], self.vertexes["right_up"]],
            self.right: [self.vertexes["right_up"], self.vertexes["right_down"]],
            self.right_down: [self.vertexes["right_down"], self.vertexes["down"]],
            self.left_down: [self.vertexes["down"], self.vertexes["left_down"]],
            self.left: [self.vertexes["left_down"], self.vertexes["left_up"]]
        }
    
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
        
        # init settler
        valid_tiles = [t for t in all_tiles.values() if t.terrain not in ["ocean", "mountain"] and t.unit is None]
        settler_tile = random.choice(valid_tiles)
        settler = Settler(settler_tile, self, first_settler=True)
        self.units = [settler]
        settler_tile.unit = settler
        self.capital = None
        self.cities = []
        self.border_tiles = []
        self.borders = []
        self.color = pygame.Color(random.randrange(0,256), random.randrange(0,256), random.randrange(0,256), 255)
        
    @property
    def tiles(self):
        results = {}
        for city in self.cities:
            for _tile in city.tiles:
                if _tile.seq not in results:
                    results[_tile.seq] = _tile
        return results
    
    def update_border_tiles(self, new_city_borders):
        self.border_tiles.extend(new_city_borders)
        valid_borders = []
        self_tiles = self.tiles
        for _border_tile in self.border_tiles:
            for _n in _border_tile.neighbors:
                if _n not in self_tiles:
                    valid_borders.append(_border_tile) # remove it from borders
                    break
        self.border_tiles = valid_borders
    
    def update_borders(self):
        borders = []
        self_tiles = self.tiles
        for _border_tile in self.border_tiles:
            for _n in _border_tile.neighbors:
                if _n.seq not in self_tiles:
                    #import pdb; pdb.set_trace()
                    borders.append(_border_tile.edges[_n])
        self.borders = borders

    def remove_unit(self, unit):
        unit.tile.unit = None
        self.units.remove(unit)
        del unit



class Unit():
    def __init__(self, unit_type, tile, owner, moves=2):
        self.type = unit_type
        self.tile = tile
        self.owner = owner
        self.pos = self.tile.pos
        self.selected = False
        self.moves = moves
        self.actions = ["do_nothing", "sleep"]

    def move_to(self, new_tile):
        self.pos = new_tile.pos
        self.tile.unit = None
        self.tile = new_tile
        self.tile.unit = self
        self.moves -= new_tile.move_consumption

    def __repr__(self) -> str:
        return f"{self.owner.name} {self.type}"


class Settler(Unit):
    def __init__(self, tile, owner, moves=2, first_settler=False):
        super().__init__("settler", tile, owner, moves)
        self.actions = ["settle"] + self.actions
        self.is_capital = False
        if first_settler == True:
            self.is_capital = True

    def settle(self):
        print(f"{self} settle called")
        capital = City(self.tile, "CAPITAL", self.owner, is_capital=self.is_capital)
        self.owner.capital = capital
        # remove unit
        self.owner.remove_unit(self)
        consumed = True
        return consumed

class City():
    def __init__(self, tile, name, owner, start_population=1, is_capital=False):
        self.name = name
        self.owner = owner
        self.owner.cities.append(self)
        self.tile = tile
        self.population = start_population
        self.is_capital = is_capital
        self.tiles = [tile] + tile.neighbors
        self.borders = tile.neighbors
        for _tile in self.tiles:
            _tile.owner = owner

        # update civ border tiles
        self.owner.update_border_tiles(self.borders)
        self.owner.update_borders()

class Tech():
    def __init__(self, name, cost, icons, unblock_bld=[]):
        self.name = name
        self.cost = cost
        self.leads_to = []
        self.dependencies = []
        self.unblock_bld = unblock_bld
        self.completed = 0
        self.in_progress = False
        self.image = pygame.image.load(f'image/techs/{name.replace(" ", "_").lower()}.webp')
        self.icons = []
        for icon in icons:
            suffix = "png" if icon.endswith("^") else "webp"
            icon = icon.replace("^", "")
            self.icons.append(pygame.image.load(f'image/icons/{icon}.{suffix}'))
    
    @property
    def status(self):
        if self.completed >= self.cost:
            return "done"
        if self.in_progress == True:
            return "researching"
        for _tech in self.dependencies:
            if _tech.status != "done":
                return "unresearchable"
        return "ready"

class Building():
    def __init__(self, name, cost, maintenance, required_tech):
        self.name = name
        self.cost = cost
        self.maintenance = maintenance
        self.required_tech = required_tech

    
