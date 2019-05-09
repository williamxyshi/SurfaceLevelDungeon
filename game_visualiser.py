import pygame
from game_map import Grid
from typing import Tuple, Optional
from game_unit import Unit
from game_overlay import Sidebar
import os


class Visualizer:
    """A class that creates and updates the screen

    === Public Attributes ===
    width:
        Width of the display
    height:
        Height of the display
    grid:
        Object that stores map information
    sidebar:
        Object that stores a list of building names and sprites
    screen:
        !!!!!
    highlight_screen:
        Screen that is slightly transparent
    """

    width: int
    height: int
    grid: Grid
    sidebar: Sidebar
    screen: pygame.Surface
    highlight_screen: pygame.Surface
    highlight_image: pygame.image

    def __init__(self, width: int, height: int, grid: Grid, sidebar: Sidebar) -> None:
        self.game_running = True
        self.width = width
        self.height = height
        self.grid = grid
        self.sidebar = sidebar
        self.screen = pygame.display.set_mode((self.width, self.height))
        #self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        # Create highlight screen
        self.highlight_screen = pygame.Surface((120, 104))
        self.highlight_screen.set_colorkey((0, 0, 0))
        highlight_image = pygame.image.load(os.path.join(os.path.dirname(__file__), 'images\\highlight.png'))
        self.highlight_screen.blit(highlight_image, (0, 0))
        self.highlight_screen.set_alpha(100)

    def render_display(self, mouse_grid_location: Tuple[int, int], mouse_sidebar_location: Optional[int], to_build: Optional[str]) -> None:
        """Render the game to the screen
        """
        """
        if self.go:
            pygame.draw.rect(self.screen, (255, 255, 255), (0, 0, self.width, self.height))
            tile = self.grid.tiles[0][0]
            pygame.draw.lines(self.screen, (0, 0, 0), False, tile.vertices[0:5], 1)
            pygame.draw.lines(self.screen, (0, 0, 0), False,
                              [tile.vertices[0], tile.vertices[5], tile.vertices[4]], 1)
            pygame.image.save(self.screen, 'pygame_hex.png')
            self.go = False
        """

        # Wipe the screen
        pygame.draw.rect(self.screen, (0, 0, 255), (0, 0, self.width, self.height))

        # Draw tile sprites
        for sublist in self.grid.tiles:
            for tile in sublist:
                if not tile.is_empty:
                    self.screen.blit(tile.land_image, (tile.vertices[0][0] - 30, tile.vertices[0][1]))
                    if tile.supported_unit is not None:
                        self.screen.blit(tile.supported_unit.unit_image, (tile.vertices[0][0] - 30, tile.vertices[0][1]))
                    elif tile.supported_building is not None:
                        self.screen.blit(tile.supported_building.building_image, (tile.vertices[0][0] - 30, tile.vertices[0][1]))

        # Draw tile outlines
        hovered_tile = None
        selected_tile = None
        highlighted_tiles = []
        x = 0
        for sublist in self.grid.tiles:
            y = 0
            for tile in sublist:
                if not tile.is_empty:
                    if tile.selected:
                        selected_tile = tile
                    elif (x, y) == mouse_grid_location and mouse_sidebar_location is None:
                        hovered_tile = tile
                    else:
                        # Use draw lines instead of draw polygon to avoid differently drawn diagonal lines
                        pygame.draw.lines(self.screen, (0, 0, 0), False, tile.vertices[0:5], 1)
                        pygame.draw.lines(self.screen, (0, 0, 0), False,
                                          [tile.vertices[0], tile.vertices[5], tile.vertices[4]], 1)
                    if tile.highlighted:
                        highlighted_tiles.append(tile)
                y += 1
            x += 1

        for tile in highlighted_tiles:
            if not tile.is_empty:
                self.screen.blit(self.highlight_screen, (tile.vertices[0][0] - 30, tile.vertices[0][1]))

        if hovered_tile is not None:
            # Use draw lines instead of draw polygon to avoid differently drawn diagonal lines
            pygame.draw.lines(self.screen, (94, 152, 152), False, hovered_tile.vertices[0:5], 1)
            pygame.draw.lines(self.screen, (94, 152, 152), False,
                              [hovered_tile.vertices[0], hovered_tile.vertices[5], hovered_tile.vertices[4]], 1)
        if selected_tile is not None:
            # Use draw lines instead of draw polygon to avoid differently drawn diagonal lines
            pygame.draw.lines(self.screen, (219, 232, 101), False, selected_tile.vertices[0:5], 3)
            pygame.draw.lines(self.screen, (219, 232, 101), False,
                              [selected_tile.vertices[0], selected_tile.vertices[5], selected_tile.vertices[4]], 3)

        # Draw sidebar
        num = 0
        for building in self.sidebar.building_info:
            rectangle = pygame.Rect(0, num*104, 120, 104)
            if num == mouse_sidebar_location:
                pygame.draw.rect(self.screen, (255, 255, 255), rectangle, 2)
            else:
                pygame.draw.rect(self.screen, (0, 0, 0), rectangle, 2)
            if to_build is not None:
                if to_build == building[0]:
                    pygame.draw.rect(self.screen, (219, 232, 101), rectangle, 3)
            self.screen.blit(building[1], (0, num*104))
            num += 1

        # update the display
        pygame.display.flip()

