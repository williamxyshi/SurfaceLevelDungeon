import pygame
from game_visualiser import Visualizer
from game_map import Grid
import csv


class Game:
    """Class that initializes the game and runs the game loop
        === Public Attributes ===
        game_running:
            True if the game is running
        visualiser:
            Object that initializes and updates the screen
        grid:
            Object that stores map information
        mouse_pressed:
            True if the mouse is pressed down
    """

    game_running: bool
    visualizer: Visualizer
    grid: Grid
    mouse_pressed: bool

    def __init__(self) -> None:
        """Initializes all components of the game
        """
        self.game_running = True
        with open('data/map.csv') as map_file:
            csv_reader = csv.reader(map_file, delimiter=',')
            grid_dimensions = next(csv_reader)
            map_lines = []
            for line in csv_reader:
                map_lines.append(line)
        self.grid = Grid(int(grid_dimensions[0]), int(grid_dimensions[1]), 60, map_lines)
        self.visualizer = Visualizer(1024, 768, self.grid)  # 1024, 768
        self.mouse_pressed = False
        pygame.init()
        self._game_loop()

    def _game_loop(self) -> None:
        mouse_grid_location = (-1, -1)
        selecting = False
        while self.game_running:
            # remove event from the event queue
            event = pygame.event.poll()

            # if the user closes the window or system asks process to quit
            if event.type == pygame.QUIT:
                self.game_running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:
                    self.mouse_pressed = True
                if event.button == 1:
                    selecting = True
            elif event.type == pygame.MOUSEBUTTONUP:
                self.mouse_pressed = False
                if selecting:
                    self.grid.select_tile(mouse_grid_location)
                    selecting = False
            elif event.type == pygame.MOUSEMOTION:
                selecting = False
                if self.mouse_pressed:
                    self.grid.pan(pygame.mouse.get_rel())
                else:
                    #  update the location of the mouse for get_rel
                    pygame.mouse.get_rel()

            # Calculate the mouse's position on the hex grid
            mouse_position = pygame.mouse.get_pos()
            mouse_grid_location = self.grid.find_mouse_grid_location(mouse_position)

            self.visualizer.render_display(mouse_grid_location)


if __name__ == '__main__':
    game = Game()
