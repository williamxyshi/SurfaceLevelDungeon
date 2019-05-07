import pygame
from game_map import Grid
from typing import Tuple

class Visualizer:
    """A class that creates and updates the screen

    === Public Attributes ===
    width:
        Width of the display
    height:
        Height of the display
    grid:
        Object that stores map information
    screen:
        !!!!!
    """

    width: int
    height: int
    grid: Grid
    screen: pygame.Surface

    def __init__(self, width: int, height: int, grid: Grid) -> None:
        self.game_running = True
        self.width = width
        self.height = height
        self.grid = grid
        self.screen = pygame.display.set_mode((self.width, self.height))

    def render_display(self, mouse_grid_location: Tuple[int, int]) -> None:
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

        # Draw tile outlines
        hovered_tile = None
        selected_tile = None
        x = 0
        for sublist in self.grid.tiles:
            y = 0
            for tile in sublist:
                if not tile.is_empty:
                    if tile.selected:
                        selected_tile = tile
                    elif (x, y) == mouse_grid_location:
                        hovered_tile = tile
                    else:
                        # Use draw lines instead of draw polygon to avoid differently drawn diagonal lines
                        pygame.draw.lines(self.screen, (0, 0, 0), False, tile.vertices[0:5], 1)
                        pygame.draw.lines(self.screen, (0, 0, 0), False,
                                          [tile.vertices[0], tile.vertices[5], tile.vertices[4]], 1)
                y += 1
            x += 1
        if hovered_tile is not None:
            # Use draw lines instead of draw polygon to avoid differently drawn diagonal lines
            pygame.draw.lines(self.screen, (255, 255, 255), False, hovered_tile.vertices[0:5], 1)
            pygame.draw.lines(self.screen, (255, 255, 255), False,
                              [hovered_tile.vertices[0], hovered_tile.vertices[5], hovered_tile.vertices[4]], 1)
        if selected_tile is not None:
            # Use draw lines instead of draw polygon to avoid differently drawn diagonal lines
            pygame.draw.lines(self.screen, (219, 232, 101), False, selected_tile.vertices[0:5], 3)
            pygame.draw.lines(self.screen, (219, 232, 101), False,
                              [selected_tile.vertices[0], selected_tile.vertices[5], selected_tile.vertices[4]], 3)

        # update the display
        pygame.display.flip()

