
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
