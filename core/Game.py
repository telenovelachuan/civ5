from . import Objects
from math import sqrt

tile_radius = Objects.TILE_RADIUS
tile_perpd = round(Objects.TILE_RADIUS / 2 * sqrt(3), 2)

def init_tiles(screen_size_x, screen_size_y):
    first_pos = (tile_perpd, tile_radius)
    first_tile = Objects.Tile(first_pos)
    results = {first_pos: first_tile}
    # centers = [first_pos]
    new_tiles_to_expand = {first_pos: first_tile}
    while len(new_tiles_to_expand) > 0:
        updated_new_tiles = {}
        for _new_pos, _new_tile in new_tiles_to_expand.items():

            # search left
            left_x, left_y = round(_new_pos[0] - tile_perpd * 2, 2), _new_pos[1]
            if left_x > 0 and (left_x, left_y) not in results: # add
                _tile = results.get((left_x, left_y), Objects.Tile((left_x, left_y))) 
                _new_tile.left = _tile
                _tile.right = _new_tile
                updated_new_tiles[(left_x, left_y)] = _tile
                results[(left_x, left_y)] = _tile
                #centers.append((left_x, left_y))

            # search right
            right_x, right_y = round(_new_pos[0] + tile_perpd * 2, 2), _new_pos[1]
            if right_x < screen_size_x and (right_x, right_y) not in results:
                _tile = results.get((right_x, right_y), Objects.Tile((right_x, right_y))) 
                _new_tile.right = _tile
                _tile.left = _new_tile
                updated_new_tiles[(right_x, right_y)] = _tile
                results[(right_x, right_y)] = _tile
                # centers.append((right_x, right_y))

            # search left up
            left_up_x, left_up_y = round(_new_pos[0] - tile_perpd, 2), round(_new_pos[1] - 1.5 * tile_radius, 2)
            if left_up_x > 0 and left_up_y > 0 and (left_up_x, left_up_y) not in results:
                _tile = results.get((left_up_x, left_up_y), Objects.Tile((left_up_x, left_up_y))) 
                _new_tile.left_up = _tile
                _tile.right_down = _tile
                updated_new_tiles[(left_up_x, left_up_y)] = _tile
                results[(left_up_x, left_up_y)] = _tile
                # centers.append((left_up_x, left_up_y))
            
            # search left down
            left_down_x, left_down_y = round(_new_pos[0] - tile_perpd, 2), round(_new_pos[1] + 1.5 * tile_radius, 2)
            if left_down_x > 0 and left_down_y < screen_size_y and (left_down_x, left_down_y) not in results:
                _tile = results.get((left_down_x, left_down_y), Objects.Tile((left_down_x, left_down_y))) 
                _new_tile.left_down = _tile
                _tile.right_up = _tile
                updated_new_tiles[(left_down_x, left_down_y)] = _tile
                results[(left_down_x, left_down_y)] = _tile
                # centers.append((left_down_x, left_down_y))

            # search right up
            right_up_x, right_up_y = round(_new_pos[0] + tile_perpd, 2), round(_new_pos[1] - 1.5 * tile_radius, 2)
            if right_up_x < screen_size_x and right_up_y > 0 and (right_up_x, right_up_y) not in results:
                _tile = results.get((right_up_x, right_up_y), Objects.Tile((right_up_x, right_up_y))) 
                _new_tile.right_up = _tile
                _tile.left_down = _tile
                updated_new_tiles[(right_up_x, right_up_y)] = _tile
                results[(right_up_x, right_up_y)] = _tile
                # centers.append((right_up_x, right_up_y))

            # search right down
            right_down_x, right_down_y = round(_new_pos[0] + tile_perpd, 2), round(_new_pos[1] + 1.5 * tile_radius, 2)
            if right_down_x < screen_size_x and right_down_y < screen_size_y and (right_down_x, right_down_y) not in results:
                _tile = results.get((right_down_x, right_down_y), Objects.Tile((right_down_x, right_down_y))) 
                _new_tile.right_down = _tile
                _tile.left_up = _tile
                updated_new_tiles[(right_down_x, right_down_y)] = _tile
                results[(right_down_x, right_down_y)] = _tile
                # centers.append((right_down_x, right_down_y))

        #updated_new_tiles = list(set(updated_new_tiles))

        new_tiles_to_expand = updated_new_tiles

    return results