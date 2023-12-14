import math
from . import Objects

DIR_OPPOSITES = {
    "left": "right",
    "right": "left",
    "left_up": "right_down",
    "right_up": "left_down",
    "right_down": "left_up",
    "left_down": "right_up"
}

def calc_route(tile1, tile2):
    new_step = tile1
    path = []
    while new_step.pos != tile2.pos:
        diff_x = tile2.pos[0] - new_step.pos[0]
        diff_y = tile2.pos[1] - new_step.pos[1]

        if abs(diff_x) > abs(diff_y): # step horizontally
            if diff_x > 0:
                new_step = new_step.right
                path.append(new_step)
            else:
                
                new_step = new_step.left
                path.append(new_step)
        elif abs(diff_x) < abs(diff_y): # step vertically
            if diff_y < 0: # moving up
                if diff_x > 0: # moving right up
                    
                    new_step = new_step.right_up
                    path.append(new_step)
                else: # moving left up
                    
                    new_step = new_step.left_up
                    path.append(new_step)
            elif diff_y > 0: # moving down
                if diff_x > 0: # moving right down
                    
                    new_step = new_step.right_down
                    path.append(new_step)
                else:
                    
                    new_step = new_step.left_down
                    path.append(new_step)
            else:
                pass
        elif diff_x == 0 and diff_y == 0:
            break
        else: # moving diagonal
            if diff_x > 0: # moving right
                new_step = new_step.right
                path.append(new_step)
            else:
                new_step = new_step.left
                path.append(new_step)

    return path


def calc_route2(tile1, tile2):
    paths = [[[tile1.left.pos], tile1.left], [[tile1.left_up.pos], tile1.left_up], [[tile1.right_up.pos], tile1.right_up],
             [[tile1.right.pos], tile1.right], [[tile1.right_down.pos], tile1.right_down], [[tile1.left_down.pos], tile1.left_down]]
    # trim invalid options
    paths = [ele for ele in paths if ele[1] is not None]
    stop = False
    while stop == False:
        paths_copy = [ele for ele in paths]
        #new_path = []
        for ele in paths:
            paths_copy.remove(ele)
            _path, dest = ele[0], ele[1]
            #import pdb; pdb.set_trace()
            if dest.pos == tile2.pos:
                stop = True
                break
            #oppo_dir = DIR_OPPOSITES[_path[-1]]
            for option in ["left", "left_up", "right_up", "right", "right_down", "left_down"]:
                new_dest = getattr(dest, option)
                if new_dest is None or new_dest.pos in _path:
                    continue
                new_search_path = _path + [new_dest.pos]
                paths_copy.append([new_search_path, new_dest])
            #import pdb; pdb.set_trace()
        paths = paths_copy
    
    #import pdb; pdb.set_trace()
    valid_paths = [ele for ele in paths if ele[1].pos == tile2.pos]
    print(f"valid_paths:{len(valid_paths)} paths")
    best_path = valid_paths[0][0]
    for _p in valid_paths:
        if len(_p[0]) < len(best_path):
            best_path = _p[0]
    print(f"best path: {best_path}")

    results = []
    cur_node = tile1
    for path_pos in best_path:
        if cur_node.pos[1] == path_pos[1]:
            if cur_node.pos[0] > path_pos[0]:
                new_node = cur_node.left
            else:
                new_node = cur_node.right
        elif path_pos[1] > cur_node.pos[1]  and path_pos[0] > cur_node.pos[0]:
            new_node = cur_node.right_down
        elif path_pos[1] > cur_node.pos[1] and path_pos[0] < cur_node.pos[0]:
            new_node = cur_node.left_down
        elif path_pos[1] < cur_node.pos[1] and path_pos[0] > cur_node.pos[0]:
            new_node = cur_node.right_up
        else:
            new_node = cur_node.left_up
        
        results.append(new_node)
        cur_node = new_node

    return results

def get_peripheral(screen, radius, tile, all_tiles):
    screen_x, screen_y = screen.get_size()
    if radius == 1:
        return tile.neighbors
    row_capacity = math.ceil(screen_x / (tile.radius * math.sqrt(3)))
    #left_most = all_tiles[str(int(tile.seq) - radius)]
    left_most = int(tile.seq) - radius
    #left_up_most = all_tiles[str(int(tile.seq) - radius * row_capacity)]
    left_up_most = int(tile.seq) - radius * row_capacity
    #right_up_most = all_tiles[str(int(tile.seq) - radius * (row_capacity - 1))]
    right_up_most = int(tile.seq) - radius * (row_capacity - 1)
    #right_most = all_tiles[str(int(tile.seq) + radius)]
    right_most = int(tile.seq) + radius
    #right_down_most = all_tiles[str(int(tile.seq) + radius * row_capacity)]
    right_down_most = int(tile.seq) + radius * row_capacity
    #left_down_most = all_tiles[str(int(tile.seq) + radius * (row_capacity - 1))]
    left_down_most = int(tile.seq) + radius * (row_capacity - 1)

    edge1 = list(range(left_most, left_up_most, -(row_capacity - 1))) # left up edge
    edge2 = list(range(left_up_most, right_up_most, 1)) # up edge
    edge3 = list(range(right_up_most, right_most, row_capacity)) # right up edge
    edge4 = list(range(right_most, right_down_most, row_capacity - 1)) # right down edge
    edge5 = list(range(right_down_most, left_down_most, -1)) # down edge
    edge6 = list(range(left_down_most, left_most, -row_capacity)) # left down edge

    all_tile_seqs = edge1 + edge2 + edge3 + edge4 + edge5 + edge6
    # remove illegal tiles
    all_tile_seqs = [seq for seq in all_tile_seqs if seq > 0 and seq < len(all_tiles)]
    right_walls = []

    return [all_tiles[str(seq)] for seq in all_tile_seqs]



def get_accessible_tiles(screen, all_tiles, tile, move):
    # results = {}
    # for _t in tile.neighbors:
    #     results[_t] = move - _t.move_consumption

    
    # search_stack = [_t for _t, _move in results.items() if _move > 0]
    # while len(search_stack) > 0:
    #     new_search_stack = []
    #     for _t in search_stack:
    #         for _n in _t.neighbors:
    #             if _n not in results:
    #                 _remaining = results[_t] - _n.move_consumption
    #                 results[_n] = _remaining
    #                 if _remaining > 0:
    #                     new_search_stack.append(_n)

    #     search_stack = new_search_stack

    #return tile.neighbors
    tiles = get_peripheral(screen, move, tile, all_tiles) 
    return tiles


def calc_moves(move_limit, path=None, tile1=None, tile2=None):
    moves = 0
    if path is None:
        path = calc_route2(tile1, tile2)
    for _tile in path:
        moves += _tile.move_consumption
        #if moves <= move_limit:
        _tile.tag = "path"
    return moves

