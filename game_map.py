import math
from typing import List, Tuple
import pygame
import os


class Tile:
    """A class that represents one tile on the game map
    === Public Attributes ===
    is_empty:
        If this object represents an empty tile
    vertices:
        Coordinates of all the vertices of the tile
    land_image:
        Sprite of the land on the tile
    selected:
        If this tile is selected
    """

    vertices: List[List[int]]
    land_image: pygame.image
    selected: bool

    def __init__(self, vertices: List[List[int]] = None, image_name: str = None) -> None:
        if vertices is None:
            self.vertices = None
            self.is_empty = True
            self.land_image = None
            self.selected = None
        else:
            self.is_empty = False
            self.vertices = vertices
            self.land_image = pygame.image.load(os.path.join(os.path.dirname(__file__), 'images\\' + image_name + '.png'))
            self.selected = False

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
    """

    tiles: List[List[Tile]]
    columns: int
    rows: int
    radius: int
    half_height: int
    xoffset: int
    yoffset: int
    selected_tile: Tile

    def __init__(self, columns: int, rows: int, radius: int, lines: List[List[str]]) -> None:
        # Create map tiles
        self.columns = columns
        self.rows = rows
        self.radius = radius
        self.half_height = round(math.sqrt(radius ** 2 - (1/2 * radius) ** 2))
        self.tiles = []
        self.xoffset = 0
        self.yoffset = 0
        self.selected_tile = None
        for _ in range(self.columns):
            self.tiles.append([])

        index_lines = 0
        for x in range(self.columns):
            shifted_x = int(x * (3 / 2) * radius + 1 / 2 * radius)
            for y in range(self.rows):
                if int(lines[index_lines][0]) == x and int(lines[index_lines][1]) == y:
                    shifted_y = y * 2 * self.half_height
                    if x % 2 == 1:
                        shifted_y += self.half_height
                    point_list = self._get_vertices(shifted_x, shifted_y)
                    new_tile = Tile(point_list, lines[index_lines][2])
                    self.tiles[x].append(new_tile)
                    if index_lines+1 < len(lines):
                        index_lines += 1
                else:
                    new_tile = Tile()
                    self.tiles[x].append(new_tile)

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

    def select_tile(self, mouse_grid_location) -> None:
        if 0 <= mouse_grid_location[0] < self.columns and 0 <= mouse_grid_location[1] < self.rows:
            clicked_tile = self.tiles[mouse_grid_location[0]][mouse_grid_location[1]]
            if (not clicked_tile.is_empty) and (self.selected_tile != clicked_tile):
                if self.selected_tile != self.tiles[mouse_grid_location[0]][mouse_grid_location[1]]:
                    if self.selected_tile:
                        self.selected_tile.selected = False
                    self.selected_tile = clicked_tile
                    self.selected_tile.selected = True
                    return None
        if self.selected_tile:
            self.selected_tile.selected = False
            self.selected_tile = None

