import pygame
from game_visualiser import Visualizer
from game_map import Grid
from game_overlay import Sidebar
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
        sidebar:
            Object that stores building names and images
    """

    game_running: bool
    visualizer: Visualizer
    grid: Grid
    sidebar: Sidebar

    def __init__(self) -> None:
        """Initializes all components of the game
        """
        self.game_running = True
        with open('data/map.csv') as map_file:
            csv_reader = csv.reader(map_file, delimiter=',')
            grid_dimensions = next(csv_reader)
            building_names = next(csv_reader)
            map_lines = []
            for line in csv_reader:
                map_lines.append(line)
        self.grid = Grid(int(grid_dimensions[0]), int(grid_dimensions[1]), 60, map_lines)
        self.sidebar = Sidebar(building_names)
        self.visualizer = Visualizer(1024, 768, self.grid)  # 1024, 768
        pygame.init()
        self._game_loop()

    def _game_loop(self) -> None:
        mouse_grid_location = (-1, -1)
        action_type = "select"
        panned = False
        right_mouse_pressed = False
        while self.game_running:
            # remove event from the event queue
            event = pygame.event.poll()

            # if the user closes the window or system asks process to quit
            if event.type == pygame.QUIT:
                self.game_running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:
                    right_mouse_pressed = True
                if event.button == 1:
                    self.grid.left_click(mouse_grid_location, action_type)
                    action_type = 'select'

            elif event.type == pygame.MOUSEBUTTONUP:
                if not panned and right_mouse_pressed:
                    self.grid.unselect()
                else:
                    panned = False
                right_mouse_pressed = False

            elif event.type == pygame.MOUSEMOTION:
                if right_mouse_pressed:
                    self.grid.pan(pygame.mouse.get_rel())
                    panned = True
                else:
                    #  update the location of the mouse for get_rel
                    pygame.mouse.get_rel()

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_e:
                    if action_type == 'build':
                        action_type = 'select'
                    else:
                        action_type = 'build'
                    self.grid.unselect()

            # Calculate the mouse's position on the hex grid
            mouse_position = pygame.mouse.get_pos()
            mouse_grid_location = self.grid.find_mouse_grid_location(mouse_position)

            self.visualizer.render_display(mouse_grid_location)


if __name__ == '__main__':
    game = Game()
