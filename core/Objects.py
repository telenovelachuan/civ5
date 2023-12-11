
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
