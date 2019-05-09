from typing import List, Tuple, Optional
import pygame
import os


class Sidebar:
    """Contains list of buildings and information to draw sidebar

    === Public Attributes ===
    building_info:
        Dictionary that stores building names and sprites
    """

    # building_info: List[str, pygame.image]

    def __init__(self, building_names: List[str]) -> None:
        self.building_info = []
        for name in building_names:
            image = pygame.image.load(os.path.join(os.path.dirname(__file__), 'images\\' + name + '.png'))
            self.building_info.append((name, image))

    def find_mouse_sidebar_location(self, mouse_position: Tuple[int, int]) -> Optional[int]:
        """Finds the sidebar coordinates of the mouse
        """
        if mouse_position[0] < 120 and mouse_position[1] < 104*len(self.building_info):
            return mouse_position[1] // 104
        else:
            return None
