import pygame
from game_visualiser import Visualizer
from game_map import Grid
from game_overlay import Sidebar
import csv
import time


class Game:
    """Class that initializes the game and runs the game loop
        === Public Attributes ===
        game_running:
            True if the game is running
        fps:
            How many times the game loop should run in a second
        visualiser:
            Object that initializes and updates the screen
        grid:
            Object that stores map information
        sidebar:
            Object that stores building information
    """

    game_running: bool
    fps: int
    visualizer: Visualizer
    grid: Grid
    sidebar: Sidebar

    def __init__(self) -> None:
        """Initializes all components of the game
        """
        self.game_running = True
        self.fps = 60
        with open('data/map.csv') as map_file:
            csv_reader = csv.reader(map_file, delimiter=',')
            grid_dimensions = next(csv_reader)
            building_names = next(csv_reader)
            map_lines = []
            for line in csv_reader:
                map_lines.append(line)
        self.sidebar = Sidebar(building_names)
        self.grid = Grid(int(grid_dimensions[0]), int(grid_dimensions[1]), 60, map_lines, self.sidebar)
        self.visualizer = Visualizer(1600, 900, self.grid, self.sidebar, self.grid.spawn_tile)  # 1024, 768
        pygame.init()
        self._game_loop()

    def _game_loop(self) -> None:
        spawning = True
        current_time = time.time()
        last_frame_time = current_time
        mouse_grid_location = (-1, -1)
        mouse_sidebar_location = None
        panned = False
        right_mouse_pressed = False
        to_build = None
        animation_tick = 0
        update_animations = False

        while self.game_running:
            # Only run the game loop fps times per second
            current_time = time.time()
            sleep_time = 1./self.fps - (current_time - last_frame_time)
            if sleep_time > 0:
                time.sleep(sleep_time)
            last_frame_time = time.time()

            if not spawning:
                # remove event from the event queue
                event = pygame.event.poll()

                # if the user closes the window or system asks process to quit
                if event.type == pygame.QUIT:
                    self.game_running = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 3:
                        right_mouse_pressed = True
                    if event.button == 1:
                        to_build = self.grid.left_click(mouse_grid_location, mouse_sidebar_location, to_build)

                elif event.type == pygame.MOUSEBUTTONUP:
                    if not panned and right_mouse_pressed:
                        self.grid.unselect()
                        to_build = None
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

            # Calculate the mouse's position on the hex grid
            mouse_position = pygame.mouse.get_pos()
            mouse_grid_location = self.grid.find_mouse_grid_location(mouse_position)
            mouse_sidebar_location = self.sidebar.find_mouse_sidebar_location(mouse_position)
            if animation_tick == 45:
                update_animations = True

            self.visualizer.render_display(mouse_grid_location, mouse_sidebar_location, to_build, update_animations)

            if animation_tick == 45:
                update_animations = False
                animation_tick = 0
            else:
                animation_tick += 1

            if spawning:
                self.spawn()
                spawning = False

    def spawn(self) -> None:
        frame = 0
        while frame < 3:
            last_frame_time = time.time()
            self.visualizer.render_spawning(frame)
            frame += 1
            current_time = time.time()
            sleep_time = 1 - (current_time - last_frame_time)
            if sleep_time > 0:
                time.sleep(sleep_time)
        self.grid.set_spawn_building()


if __name__ == '__main__':
    game = Game()
