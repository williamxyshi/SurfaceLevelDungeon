import math
from typing import List, Tuple, Optional
#from __future__ import annotations
import pygame
import os
from game_unit import Unit

class Tile:
    """Tile on the game map
    === Public Attributes ===
    is_empty:
        If this object represents an empty tile
    vertices:
        Coordinates of all the vertices of the tile
    adjacent_tiles:
        All tiles adjacent to this one
    land_image:
        Sprite of the land on the tile
    selected:
        If this tile is selected
    highlighted:
        If this tile is highlighted
    building:
        If this tile is a building
    supported_unit:
        Unit on this tile
    """

    vertices: List[List[int]]
    #adjacent_tiles: List[Tile]
    land_image: pygame.image
    selected: bool
    highlighted: bool
    building: bool
    supported_unit: Unit

    def __init__(self, vertices: List[List[int]] = None, land_name: str = None, building: bool = False, supported_unit: Unit = None) -> None:
        if vertices is None:
            self.vertices = None
            self.is_empty = True
            self.land_image = None
            self.selected = None
            self.highlighted = None
        else:
            self.is_empty = False
            self.vertices = vertices
            self.land_image = pygame.image.load(os.path.join(os.path.dirname(__file__), 'images\\' + land_name + '.png'))
            self.selected = False
            self.highlighted = False
        self.building = building
        self.adjacent_tiles = []
        self.supported_unit = supported_unit
        print(self.supported_unit)

    def pan(self, movement: Tuple[int, int]) -> None:
        """Update the vertices of a tile after a pan
        """
        for vertex in self.vertices:
            vertex[0] += movement[0]
            vertex[1] += movement[1]


class Grid:
    """A class that contains all tiles in the game map
    === Public Attributes ===
    tiles:
        Array of all the tiles
    columns:
        Number of columns in the grid
    rows:
        Number of rows in the grid
    radius:
        Radius of a hexagon tile
    half_height:
        Half of the height of a hexagon tile
    xoffset:
        Number of pixels the map is shifted in the x direction
    yoffset:
        Number of pixels the map is shifted in the y direction
    selected_tile:
        Tile that is currently selected
    selected_unit:
        Unit that is currently selected
    """

    tiles: List[List[Tile]]
    columns: int
    rows: int
    radius: int
    half_height: int
    xoffset: int
    yoffset: int
    selected_tile: Tile
    selected_unit: Unit

    def __init__(self, columns: int, rows: int, radius: int, lines: List[List[str]]) -> None:
        # Create map tiles
        self.columns = columns
        self.rows = rows
        self.radius = radius
        self.half_height = round(math.sqrt(radius ** 2 - (1/2 * radius) ** 2))
        self.tiles = []
        self.buildings = []
        self.xoffset = 0
        self.yoffset = 0
        self.selected_tile = None
        self.selected_unit = None
        for _ in range(self.columns):
            self.tiles.append([])

        # Create tile objects and append them to the correct location in tiles
        index_lines = 0
        for x in range(self.columns):
            shifted_x = int(x * (3 / 2) * radius + 1 / 2 * radius)
            for y in range(self.rows):
                if int(lines[index_lines][0]) == x and int(lines[index_lines][1]) == y:
                    shifted_y = y * 2 * self.half_height
                    if x % 2 == 1:
                        shifted_y += self.half_height
                    point_list = self._get_vertices(shifted_x, shifted_y)
                    if lines[index_lines][3] != 'None':
                        new_unit = Unit(lines[index_lines][3])
                    else:
                        new_unit = None
                    new_tile = Tile(point_list, lines[index_lines][2], False, new_unit)
                    self.tiles[x].append(new_tile)
                    if index_lines+1 < len(lines):
                        index_lines += 1
                else:
                    new_tile = Tile()
                    self.tiles[x].append(new_tile)

        # Update all the tile's adjacent tile attribute
        for x in range(self.columns):
            for y in range(self.rows):
                current_tile = self.tiles[x][y]
                if not current_tile.is_empty:
                    if x % 2 == 0:
                        if 0 <= x - 1 < self.columns and 0 <= y - 1 < self.rows:
                            current_tile.adjacent_tiles.append(self.tiles[x-1][y-1])
                        if 0 <= y - 1 < self.rows:
                            current_tile.adjacent_tiles.append(self.tiles[x][y-1])
                        if 0 <= x + 1 < self.columns and 0 <= y - 1 < self.rows:
                            current_tile.adjacent_tiles.append(self.tiles[x+1][y-1])
                        if 0 <= x + 1 < self.columns:
                            current_tile.adjacent_tiles.append(self.tiles[x+1][y])
                        if 0 <= y + 1 < self.rows:
                            current_tile.adjacent_tiles.append(self.tiles[x][y+1])
                        if 0 <= x - 1 < self.columns:
                            current_tile.adjacent_tiles.append(self.tiles[x-1][y])
                    else:
                        if 0 <= x - 1 < self.columns:
                            current_tile.adjacent_tiles.append(self.tiles[x-1][y])
                        if 0 <= y - 1 < self.rows:
                            current_tile.adjacent_tiles.append(self.tiles[x][y-1])
                        if 0 <= x + 1 < self.columns:
                            current_tile.adjacent_tiles.append(self.tiles[x+1][y])
                        if 0 <= x + 1 < self.columns and 0 <= y + 1 < self.rows:
                            current_tile.adjacent_tiles.append(self.tiles[x+1][y+1])
                        if 0 <= y + 1 < self.rows:
                            current_tile.adjacent_tiles.append(self.tiles[x][y+1])
                        if 0 <= x - 1 < self.columns and 0 <= y + 1 < self.rows:
                            current_tile.adjacent_tiles.append(self.tiles[x-1][y+1])

    def _get_vertices(self, x: int, y: int) -> List[Tuple[int, int]]:
        """Uses the coordinates of the top right point of a hexagon to calculate the remaining points
        """
        point_list = [[x, y]]  # top left point
        point_list.append([x + self.radius, y])  # top right point
        point_list.append([int(x + 3 / 2 * self.radius), y + self.half_height])  # rightmost point
        point_list.append([x + self.radius, y + 2 * self.half_height])  # bottom right point
        point_list.append([x, y + 2 * self.half_height])  # bottom left point
        point_list.append([int(x - self.radius / 2), y + self.half_height])  # leftmost point
        return point_list

    def find_mouse_grid_location(self, mouse_position: Tuple[int, int]) -> Tuple[int, int]:
        """Finds the grid coordinates of the mouse
        """
        mousex = mouse_position[0] - self.xoffset
        mousey = mouse_position[1] - self.yoffset
        mouse_grid_x = int(mousex // (3 / 2 * self.radius))
        tile_x = mousex % (3 / 2 * self.radius)
        tile_y = mousey % (2 * self.half_height)
        if mouse_grid_x % 2 == 1 and tile_x < (-self.radius / (2 * self.half_height) * abs(tile_y - self.half_height) + 1 / 2 * self.radius):
            mouse_grid_x -= 1
        elif mouse_grid_x % 2 == 0 and tile_x < (self.radius / (2 * self.half_height) * abs(tile_y - self.half_height)):
            mouse_grid_x -= 1
        if mouse_grid_x % 2 == 0:
            mouse_grid_y = int(mousey // (2 * self.half_height))
        else:
            mouse_grid_y = int((mousey - self.half_height) // (2 * self.half_height))
        return mouse_grid_x, mouse_grid_y

    def pan(self, movement: Tuple[int, int]) -> None:
        """Update the offset caused by a pan for the grid and all tiles"""
        self.xoffset += movement[0]
        self.yoffset += movement[1]
        for sublist in self.tiles:
            for tile in sublist:
                if not tile.is_empty:
                    tile.pan(movement)

    def select(self, mouse_grid_location: Tuple[int, int], action_type: str) -> None:
        clicked_tile = self._find_clicked_tile(mouse_grid_location)
        if action_type == 'select':
            if clicked_tile is not None and self.selected_tile != clicked_tile:
                if clicked_tile.highlighted and self.selected_unit is not None:
                    clicked_tile.supported_unit = self.selected_unit
                    self.selected_tile.supported_unit = None
                self.unselect()
                self.selected_tile = clicked_tile
                self.selected_tile.selected = True
                if self.selected_tile.supported_unit is not None:
                    self.selected_unit = self.selected_tile.supported_unit
                    for tile in self.selected_tile.adjacent_tiles:
                        if not tile.is_empty:
                            tile.highlighted = True
            elif self.selected_tile is not None:
                self.unselect()

        elif action_type == 'build':
            if clicked_tile is not None:
                if not clicked_tile.building and clicked_tile.supported_unit is None:
                    clicked_tile.building = True
                    clicked_tile.land_image = pygame.image.load(os.path.join(os.path.dirname(__file__), 'images\\' + 'tower_test' + '.png'))

    def unselect(self) -> None:
        if self.selected_tile is not None:
            self.selected_tile.selected = False
            for tile in self.selected_tile.adjacent_tiles:
                if not tile.is_empty:
                    tile.highlighted = False
        self.selected_tile = None

    def _find_clicked_tile(self, mouse_grid_location: Tuple[int, int]) -> Optional[Tile]:
        if 0 <= mouse_grid_location[0] < self.columns and 0 <= mouse_grid_location[1] < self.rows:
            clicked_tile = self.tiles[mouse_grid_location[0]][mouse_grid_location[1]]
            if not clicked_tile.is_empty:
                return clicked_tile
        return None
