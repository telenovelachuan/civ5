
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
    def production(self):
        if self.terrain == "hill":
            return 2
        elif self.terrain == "plain":
            return 1
        return 0
