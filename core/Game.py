from . import Objects
from math import sqrt
import random

LAND_SEED_NUM = 2

tile_radius = Objects.TILE_RADIUS
tile_perpd = round(Objects.TILE_RADIUS / 2 * sqrt(3), 2)

def init_tiles(screen_size_x, screen_size_y):
    first_pos = (tile_perpd, tile_radius)
    first_tile = Objects.Tile(first_pos)
    results = {first_pos: first_tile}
    new_tiles_to_expand = {first_pos: first_tile}
    while len(new_tiles_to_expand) > 0:
        updated_new_tiles = {}
        for _new_pos, _new_tile in new_tiles_to_expand.items():
            # search left
            left_x, left_y = round(_new_pos[0] - tile_perpd * 2, 2), _new_pos[1]
            if left_x > 0:
                created_tile = Objects.Tile((left_x, left_y))
                if (left_x, left_y) not in results: # add
                    updated_new_tiles[(left_x, left_y)] = created_tile

                _tile = results.get((left_x, left_y), created_tile) 
                _new_tile.left = _tile
                _tile.right = _new_tile     
                results[(left_x, left_y)] = _tile

            # search right
            right_x, right_y = round(_new_pos[0] + tile_perpd * 2, 2), _new_pos[1]
            if right_x < screen_size_x:
                created_tile = Objects.Tile((right_x, right_y))
                if (right_x, right_y) not in results:
                    updated_new_tiles[(right_x, right_y)] = created_tile

                _tile = results.get((right_x, right_y), created_tile) 
                _new_tile.right = _tile
                _tile.left = _new_tile
                results[(right_x, right_y)] = _tile

            # search left up
            left_up_x, left_up_y = round(_new_pos[0] - tile_perpd, 2), round(_new_pos[1] - 1.5 * tile_radius, 2)
            if left_up_x > 0 and left_up_y > 0:
                created_tile = Objects.Tile((left_up_x, left_up_y))
                if (left_up_x, left_up_y) not in results:
                    updated_new_tiles[(left_up_x, left_up_y)] = created_tile
                _tile = results.get((left_up_x, left_up_y), created_tile) 
                _new_tile.left_up = _tile
                _tile.right_down = _new_tile
                results[(left_up_x, left_up_y)] = _tile
            
            # search left down
            left_down_x, left_down_y = round(_new_pos[0] - tile_perpd, 2), round(_new_pos[1] + 1.5 * tile_radius, 2)
            if left_down_x > 0 and left_down_y < screen_size_y:
                created_tile = Objects.Tile((left_down_x, left_down_y))
                if (left_down_x, left_down_y) not in results:
                    updated_new_tiles[(left_down_x, left_down_y)] = created_tile
                _tile = results.get((left_down_x, left_down_y), created_tile) 
                _new_tile.left_down = _tile
                _tile.right_up = _new_tile
                results[(left_down_x, left_down_y)] = _tile

            # search right up
            right_up_x, right_up_y = round(_new_pos[0] + tile_perpd, 2), round(_new_pos[1] - 1.5 * tile_radius, 2)
            if right_up_x < screen_size_x and right_up_y > 0:
                created_tile = Objects.Tile((right_up_x, right_up_y))
                if (right_up_x, right_up_y) not in results:
                    updated_new_tiles[(right_up_x, right_up_y)] = created_tile
                _tile = results.get((right_up_x, right_up_y), created_tile) 
                _new_tile.right_up = _tile
                _tile.left_down = _new_tile
                
                results[(right_up_x, right_up_y)] = _tile

            # search right down
            right_down_x, right_down_y = round(_new_pos[0] + tile_perpd, 2), round(_new_pos[1] + 1.5 * tile_radius, 2)
            if right_down_x < screen_size_x and right_down_y < screen_size_y:
                created_tile = Objects.Tile((right_down_x, right_down_y))
                if (right_down_x, right_down_y) not in results:
                    updated_new_tiles[(right_down_x, right_down_y)] = created_tile
                _tile = results.get((right_down_x, right_down_y), created_tile) 
                _new_tile.right_down = _tile
                _tile.left_up = _new_tile
                results[(right_down_x, right_down_y)] = _tile

        new_tiles_to_expand = updated_new_tiles
    return results

def init_terrain(tiles):
    # randomize 2 large continents
    land_seeds = random.sample(list(tiles.values()), LAND_SEED_NUM)
    tiles_to_assign = []
    for _tile in land_seeds:
        _tile.terrain = "grassland"
        tiles_to_assign.extend(_tile.neighbors)

    vicinity = 1
    while len(tiles_to_assign) > 0:
        new_tiles_to_assign = []
        for _tile in tiles_to_assign:
            if _tile.terrain is not None:
                continue

            _terrain = "land" if random.random() >= vicinity * 0.10 else "ocean"
            if _terrain == "land":
                # grassland, mountain, desert, plain, jungle
                _random = random.random()
                if _random <= 0.1:
                    _terrain = "mountain"
                elif _random > 0.1 and _random <= 0.3:
                    _terrain = "desert"
                elif _random > 0.3 and _random <= 0.5:
                    _terrain = "jungle"
                elif _random > 0.5 and _random <= 0.75:
                    _terrain = "grassland"
                else:
                    _terrain = "plain"

            _tile.terrain = _terrain
            
            existing_pos = [t.pos for t in new_tiles_to_assign]
            new_tiles_to_assign.extend([t for t in _tile.neighbors if t.terrain is None and t.pos not in existing_pos])
        
        vicinity += 1
        tiles_to_assign = new_tiles_to_assign
    
    return tiles