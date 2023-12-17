import pygame
from . import Utils

accessible_tiles_temp = None
dragging = False

def handle_events(screen, unit_circles, all_tiles, all_hexes):
    running = True
    ev = pygame.event.get()
    global dragging

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
                selected_unit = [u for u in unit_circles.keys() if u.selected == True]
                if len(selected_unit) == 0:
                    pass
                else:
                    selected_unit = selected_unit[0]
                    for _seq, _tile in all_tiles.items():
                        _hex_obj = all_hexes[_seq]
                        if _hex_obj.collidepoint(pygame.mouse.get_pos()):
                            
                            accessible_tiles = Utils.get_accessible_tiles(screen, all_tiles, selected_unit.tile, selected_unit.moves)
                            global accessible_tiles_temp
                            accessible_tiles_temp = accessible_tiles
                            for _tile in accessible_tiles:
                                _tile.tag = "path"
                        
                            if _tile in accessible_tiles:
                                dragging = True

                            
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 3: # right click up
            dragging = False
            for _seq, _tile in all_tiles.items():
                _hex_obj = all_hexes[_seq]
                if _tile.tag in ["path", "dragged"]:
                    _tile.tag = None

            selected_unit = [u for u in unit_circles.keys() if u.selected == True]
            if len(selected_unit) > 0:
                selected_unit = selected_unit[0]
                for _seq, _hex in all_hexes.items():
                    if _hex.collidepoint(pygame.mouse.get_pos()):
                        _selected_tile = all_tiles[_seq]
                        if _selected_tile in accessible_tiles_temp:
                            selected_unit.move_to(_selected_tile)
            dragging = False

        elif event.type == pygame.MOUSEMOTION:
            if dragging == True:
                for _tile in accessible_tiles_temp:
                    _tile.tag = "path"

                for _seq, _hex in all_hexes.items():
                    if _hex.collidepoint(pygame.mouse.get_pos()):
                        _selected_tile = all_tiles[_seq]
                        if _selected_tile in accessible_tiles_temp:
                            _selected_tile.tag = "dragged"

    return running