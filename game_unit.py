import pygame
import os


class Unit:
    """Unit on the game map

    === Public Attributes ===
    unit_image:
        Sprite of the unit
    """

    unit_image: pygame.image

    def __init__(self, unit_name: str) -> None:
        self.unit_image = pygame.image.load(os.path.join(os.path.dirname(__file__), 'images\\' + unit_name + '.png'))