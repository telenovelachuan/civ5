import pygame
from . import Utils

def handle_events(screen, unit_circles, all_tiles, all_hexes):
    running = True
    ev = pygame.event.get()
    for event in ev:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            #import pdb; pdb.set_trace()
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # left click
                for _unit, _circle in unit_circles.items():
                    if _circle.collidepoint(pygame.mouse.get_pos()):
                        print(f"{_unit.owner.name} {_unit.type} clicked")
                        _unit.selected = True
                    else:
                        _unit.selected = False
            elif event.button == 3: # right click, move
                #selected_unit = Game.get_selected_unit(unit_circles)
                selected_unit = [u for u in unit_circles.keys() if u.selected == True]
                if len(selected_unit) == 0:
                    pass
                else:
                    selected_unit = selected_unit[0]
                    for _seq, _tile in all_tiles.items():
                        _hex_obj = all_hexes[_seq]
                        if _hex_obj.collidepoint(pygame.mouse.get_pos()):
                            # print(f"moving unit {selected_unit.owner.name} {selected_unit.type} from {selected_unit.pos} to {_tile.pos}")
                            # path = Utils.calc_route2(selected_unit.tile, _tile)
                            # _ = Utils.calc_moves(selected_unit.moves, tile1=selected_unit.tile, tile2=_tile)
                            accessible_tiles = Utils.get_accessible_tiles(screen, all_tiles, selected_unit.tile, 4)
                            for _tile in accessible_tiles:
                                _tile.tag = "path"
                            print([t.pos for t in accessible_tiles])
                            # print(f"routed path: {path}")
                            # selected_unit.move_to(_tile)
        elif event.type == pygame.MOUSEBUTTONUP:
            for _seq, _tile in all_tiles.items():
                _hex_obj = all_hexes[_seq]
                if _tile.tag == "path":
                    _tile.tag = None
                            

    return running