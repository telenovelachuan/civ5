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

def get_peripheral(screen, all_tiles, tile, radius, ignore_terrain=True):
    seq_x, seq_y = tile.seq.split("^")
    seq_x, seq_y = float(seq_x), float(seq_y)
    results = []
    if radius == 0:
        return [tile]
    if radius == 1:
        return tile.neighbors
    
    results.append(f"{seq_x:g}^{seq_y - radius:g}")
    results.append(f"{seq_x:g}^{seq_y + radius:g}")
    for _n in range(1, radius + 1):
        results.append(f"{seq_x + _n:g}^{seq_y - radius + 0.5 * _n:g}")
        results.append(f"{seq_x + _n:g}^{seq_y + radius - _n * 0.5:g}")
        results.append(f"{seq_x - _n:g}^{seq_y - radius + 0.5 * _n:g}")
        results.append(f"{seq_x - _n:g}^{seq_y + radius - _n * 0.5:g}")

    up_corners = [r for r in results if float(r.split("^")[0]) == seq_x - radius]
    up_corner_ys = [float(r.split("^")[1]) for r in up_corners]
    min_y, max_y = min(up_corner_ys), max(up_corner_ys)
    y_range = [y / 10 for y in range(int(10 * min_y), int(10 * max_y), 5)]
    up_edge = [f"{seq_x - radius:g}^{_y:g}" for _y in y_range]
    results.extend(up_edge)

    down_corners = [r for r in results if float(r.split("^")[0]) == seq_x + radius]
    down_corner_ys = [float(r.split("^")[1]) for r in down_corners]
    min_y, max_y = min(down_corner_ys), max(down_corner_ys)
    y_range = [y / 10 for y in range(int(10 * min_y), int(10 * max_y), 5)]
    down_edge = [f"{seq_x + radius:g}^{_y:g}" for _y in y_range]
    results.extend(down_edge)

    results = list(set(results))
    results = [r for r in results if r in all_tiles]
    results = [all_tiles[seq] for seq in results]
    if ignore_terrain == False:
        results = [r for r in results if r.terrain != "mountain"]

    return results


# def get_right_wall(screen_x, tile_radius, num_all_tiles):
#     row_capacity = math.ceil(screen_x / (tile_radius * math.sqrt(3)))
#     cur_seq = row_capacity - 1 # start from 0
#     last_seq = num_all_tiles - 1
#     results = [cur_seq]
#     step = 24
#     while cur_seq <= last_seq:
#         cur_seq += step
#         results.append(cur_seq)
#         step = 25 if step == 24 else 24
#         if cur_seq == last_seq:
#             break
#     return results
    


def get_accessible_tiles(screen, all_tiles, tile, move):
    results = {tile: move}
    previous_ring = [tile]
    for _n in range(1, move + 1):
        if all([_m <= 0 for _m in results.values()]) == True:
            break
        ring = get_peripheral(screen, all_tiles, tile, _n, ignore_terrain=False)
        for _tile in ring:
            # skip if not accessible
            for _pre_tile in previous_ring:
                
                if _tile not in _pre_tile.neighbors:
                    continue
                new_moves = results[_pre_tile] - _tile.move_consumption
                if _tile in results:
                    results[_tile].append(new_moves)
                else:
                    results[_tile] = [new_moves]
        for _t, _m in results.items():
            results[_t] = _m if isinstance(_m, int) else max(_m)  # get the least consumption move

        previous_ring = [r for r in ring if r in results and results[r] > 0]

    return results.keys()


# def calc_moves(move_limit, path=None, tile1=None, tile2=None):
#     moves = 0
#     if path is None:
#         path = calc_route2(tile1, tile2)
#     for _tile in path:
#         moves += _tile.move_consumption
#         #if moves <= move_limit:
#         _tile.tag = "path"
#     return moves

