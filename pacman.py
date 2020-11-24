import pygame

from mob import Mob
from field import Field
from config import *


class Pacman(Mob):
    def __init__(self, screen: pygame.display, field: Field, coords: tuple = (10, 10)):
        super().__init__('pacman_30', PACMAN_SIZE, screen, field, coords)
        self._animation_die = dict()
        for direction in ['up', 'down', 'left', 'right']:
            self._animation_die[direction] = \
                [pygame.image.load(f"{PATH_IMAGE}\\{direction}\\pacman_dead_30_{i}.png")
                 for i in range(0, 12) for j in range(5)]

    def die(self, tick_cnt: int):
        """
        Show that pacman is dead
        :param tick_cnt: time counter for animations
        """
        animation_set = self._animation_die[self.previous_movement]
        self.screen.blit(animation_set[tick_cnt], self.coords)
