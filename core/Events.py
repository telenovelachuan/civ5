import pygame
from . import Utils

accessible_tiles_temp = None
dragging = False
selected_unit = None

def _handle_tech_circle_click(tech_circle):
    if tech_circle.collidepoint(pygame.mouse.get_pos()):
        print("tech circle clicked!!")
        return {"running": True, "drawing_mode": "tech"}
    return None

def handle_normal_events(screen, unit_circles, all_tiles, all_hexes, action_btns, tech_circle, city_banners):
    running = True
    drawing_mode = "normal"
    ev = pygame.event.get()
    global dragging
    global selected_unit
    for event in ev:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            #import pdb; pdb.set_trace()
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # left click
                if action_btns is not None:
                    for _action, _btn in action_btns.items():
                        if _btn.collidepoint(pygame.mouse.get_pos()):
                            print(f" {_action} clicked for {selected_unit}")
                            consumed = getattr(selected_unit, _action)()
                            if consumed == True:
                                selected_unit = None
                            return {"running": True, "drawing_mode": drawing_mode}

                selected_unit = None
                for _unit, _circle in unit_circles.items():
                    if _circle.collidepoint(pygame.mouse.get_pos()):
                        print(f"{_unit.owner.name} {_unit.type} clicked")
                        selected_unit = _unit
                        _unit.selected = True
                    else:
                        _unit.selected = False

                _tech_circle_click_return = _handle_tech_circle_click(tech_circle)
                if _tech_circle_click_return is not None:
                    return _tech_circle_click_return

                for _city, _banner in city_banners.items():
                    if _banner.collidepoint(pygame.mouse.get_pos()):
                        print(f"city {_city.name} banner clicked")
                        return {"running": True, "drawing_mode": "city", "city_banner_clicked": _city}
            
            elif event.button == 3: # right click, move
                if selected_unit is None:
                    pass
                else:
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

            if selected_unit is not None:
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

    
    results = {"running": running, "drawing_mode": drawing_mode}
    return results

def handle_tech_events(btn_return):
    running = True
    drawing_mode = "tech"
    ev = pygame.event.get()
    for event in ev:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            #import pdb; pdb.set_trace()
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # left click
                if btn_return.collidepoint(pygame.mouse.get_pos()):
                    drawing_mode = "normal"
    return {"running": running, "drawing_mode": drawing_mode}

def handle_city_events(tech_circle):
    running = True
    drawing_mode = "city"
    ev = pygame.event.get()
    for event in ev:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            #import pdb; pdb.set_trace()
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # left click
            _tech_circle_click_return = _handle_tech_circle_click(tech_circle)
            if _tech_circle_click_return is not None:
                return _tech_circle_click_return
    return {"running": running, "drawing_mode": drawing_mode}
