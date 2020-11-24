import pygame
from typing import Tuple

from config import *
from field import Field, back_direction
from field_config_relations import teleport


class Mob:

    def __init__(self, mob_name: str, mob_size: Tuple[int, int], screen: pygame.display,
                 field: Field, coords: Tuple[int, int] = (100, 20)):

        self._animation = dict()
        for direction in ['up', 'down', 'left', 'right']:
            self._animation[direction] = \
                [pygame.image.load(f"{PATH_IMAGE}\\{direction}\\{mob_name}_{i}.png") for i in range(0, 4)]

        self.mob_size = mob_size
        self.screen = screen
        self.field = field

        self.center = coords
        self.coords = (coords[0] - mob_size[0] // 2, coords[1] - mob_size[1] // 2)

        self.previous_movement = 'right'

    def _move(self, move_value: Tuple[int, int]):
        """
        Changes mob coordinates
        :param move_value: (x_movement, y_movement)
        """
        new_coords = (self.coords[0] + move_value[0], self.coords[1] + move_value[1])
        new_center = (self.center[0] + move_value[0], self.center[1] + move_value[1])
        if new_center in teleport:
            new_center = teleport[new_center]
            new_coords = (new_center[0] - self.mob_size[0] // 2, new_center[1] - self.mob_size[1] // 2)
        if 0 < new_coords[0] < SCREEN_SIZE[0] - self.mob_size[0] and \
                0 < new_coords[1] < SCREEN_SIZE[1] - self.mob_size[1]:
            self.coords = new_coords
            self.center = new_center

    def move(self, last_command: str, tick_cnt: int):
        """
        Sets animation according to the last_command, shows it, checks if it is possible to go to the chosen direction
        :param last_command: directon where the mob intents to to
        :param tick_cnt: time counter for animations
        """
        animation_set = self._animation['right']
        if last_command != '':
            is_corner = self.field.is_corner(self.center)
            move_value = None
            current_movement = ''
            for direction in ['up', 'down', 'left', 'right']:
                if (last_command == direction
                    and not is_corner
                    and (self.previous_movement == direction or self.previous_movement == back_direction(direction))) \
                        or (self.previous_movement == direction
                            and not is_corner
                            and last_command != back_direction(direction)) \
                        or (self.previous_movement == direction
                            and is_corner
                            and self.field.corners[self.center].directions[direction] is not None
                            and not self.field.corners[self.center].if_possible_to_go(last_command)) \
                        or (last_command == direction
                            and is_corner
                            and self.field.corners[self.center].directions[direction] is not None):
                    current_movement = direction
                    animation_set = self._animation[direction]

            if current_movement == 'up':
                move_value = (0, -1)
            elif current_movement == 'down':
                move_value = (0, 1)
            elif current_movement == 'left':
                move_value = (-1, 0)
            elif current_movement == 'right':
                move_value = (1, 0)

            if move_value is not None:
                self._move(move_value)
                self.previous_movement = current_movement

        self.screen.blit(animation_set[tick_cnt // 15], self.coords)

    def show_not_moving(self, tick_cnt: int):
        """
        Show animation without changing coordinates
        :param tick_cnt: time counter for animations
        """
        animation_set = self._animation[self.previous_movement]
        self.screen.blit(animation_set[tick_cnt // 15], self.coords)
