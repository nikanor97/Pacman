import pygame
import random
import re
from typing import Tuple

from mob import Mob
from pacman import Pacman
from field import Field, calculate_distance, back_direction
from config import *
from field_config_points import dead_end_points


class Ghost(Mob):
    _last_red_ghost_coords = (0, 0)

    def __init__(self, ghost_name: str, screen: pygame.display, field: Field, pacman: Pacman,
                 coords: tuple = (10, 10)):
        super().__init__(ghost_name, GHOST_SIZE, screen, field, coords)
        self.pacman = pacman
        self.ghost_name = ghost_name
        self.difficulty = ''

    def set_difficulty(self, difficulty: str):
        self.difficulty = difficulty

    def move_function(self, tick_cnt: int, critical_distance: int = 10) -> bool:
        """
        Chooses move function between "good strategy" movement and random movement and makes ghost move according to
        the chosen scenario
        :param tick_cnt: time counter for animations
        :param critical_distance: if the center of the ghost is less far to the pacman center than the critical
            distance, the pacman is considered to be eaten
        :return: if pacman is eaten
        """
        move_func = None
        if self.difficulty == 'Hard':
            if re.match('ghost_red', self.ghost_name) is not None:
                move_func = random.choice([self.move_red, self.move_randomly])
                self._last_red_ghost_coords = self.center
            elif re.match('ghost_blue', self.ghost_name) is not None:
                move_func = random.choice([self.move_blue, self.move_randomly])
            elif re.match('ghost_pink', self.ghost_name) is not None:
                move_func = random.choice([self.move_pink, self.move_randomly])
            elif re.match('ghost_orange', self.ghost_name) is not None:
                move_func = random.choice([self.move_orange, self.move_randomly])
        elif self.difficulty == 'Easy':
            move_func = self.move_randomly
        return move_func(tick_cnt, critical_distance)

    def change_direction_on_corners(self):
        """
        Randomly changes direction on corners
        :return: new direction
        """
        point = self.field.corners[self.center]
        possible_direction = None
        if self.center not in dead_end_points:
            while True:
                possible_direction = random.choice(['up', 'down', 'left', 'right'])
                if point.directions[possible_direction] is not None \
                        and self.previous_movement != back_direction(possible_direction):
                    break
        else:
            if self.center == dead_end_points[0]:
                possible_direction = 'right'
            elif self.center == dead_end_points[1]:
                possible_direction = 'left'
        return possible_direction

    def _calculate_target(self, pacman_shift: int):
        """
        Calulates coordinates of point which is <pacman_shift> steps further than pacman
        :param pacman_shift: number of steps
        :return: target coordinates
        """
        target_point = None
        if self.pacman.previous_movement == 'up':
            target_point = (self.pacman.center[0], self.pacman.center[1] - 18 * pacman_shift)
        elif self.pacman.previous_movement == 'down':
            target_point = (self.pacman.center[0], self.pacman.center[1] + 18 * pacman_shift)
        elif self.pacman.previous_movement == 'left':
            target_point = (self.pacman.center[0] - 22.5 * pacman_shift, self.pacman.center[1])
        elif self.pacman.previous_movement == 'right':
            target_point = (self.pacman.center[0] + 22.5 * pacman_shift, self.pacman.center[1])
        return target_point

    def _follow_target(self, coord: Tuple[int, int]):
        """
        Chooses the direction which is better to reach the coord
        :param coord: coordinates that we want to reach
        :return: direction which is better to reach the coord
        """
        result_direction = None
        if self.center not in dead_end_points:
            point = self.field.corners[self.center]
            direction_distance = dict()
            if point.directions['up'] is not None and self.previous_movement != 'down':
                new_point_coord = (point.coord[0], point.coord[1] - 18)
                direction_distance['up'] = calculate_distance(coord, new_point_coord)
            if point.directions['down'] is not None and self.previous_movement != 'up':
                new_point_coord = (point.coord[0], point.coord[1] + 18)
                direction_distance['down'] = calculate_distance(coord, new_point_coord)
            if point.directions['left'] is not None and self.previous_movement != 'right':
                new_point_coord = (point.coord[0] - 25, point.coord[1])
                direction_distance['left'] = calculate_distance(coord, new_point_coord)
            if point.directions['right'] is not None and self.previous_movement != 'left':
                new_point_coord = (point.coord[0] + 25, point.coord[1])
                direction_distance['right'] = calculate_distance(coord, new_point_coord)
            result_direction = min(direction_distance, key=direction_distance.get)
        else:
            if self.center == dead_end_points[0]:
                result_direction = 'right'
            elif self.center == dead_end_points[1]:
                result_direction = 'left'
        return result_direction

    def move_red(self, tick_cnt: int, critical_distance: int = 10):
        """
        Implements winning strategy of the red ghost
        :param tick_cnt: time counter for animations
        :param critical_distance: if the center of the ghost is less far to the pacman center than the critical
            distance, the pacman is considered to be eaten
        :return: if pacman is eaten
        """
        if self.is_pacman_eaten(critical_distance):
            return True
        if self.field.is_corner(self.center):
            target_point = self._calculate_target(1)
            result_direction = self._follow_target(target_point)
            self.move(result_direction, tick_cnt)
        else:
            self.move(self.previous_movement, tick_cnt)
        return False

    def move_blue(self, tick_cnt: int, critical_distance: int = 10):
        """
        Implements winning strategy of the blue ghost
        :param tick_cnt: time counter for animations
        :param critical_distance: if the center of the ghost is less far to the pacman center than the critical
            distance, the pacman is considered to be eaten
        :return: if pacman is eaten
        """
        if self.is_pacman_eaten(critical_distance):
            return True
        if self.field.is_corner(self.center):
            target_point = self._calculate_target(2)
            x_diff = target_point[0] - self._last_red_ghost_coords[0]
            y_diff = target_point[1] - self._last_red_ghost_coords[1]
            new_target_point = (self._last_red_ghost_coords[0] + x_diff * 2,
                                self._last_red_ghost_coords[1] + y_diff * 2)
            result_direction = self._follow_target(new_target_point)
            self.move(result_direction, tick_cnt)
        else:
            self.move(self.previous_movement, tick_cnt)
        return False

    def move_pink(self, tick_cnt: int, critical_distance: int = 10):
        """
        Implements winning strategy of the pink ghost
        :param tick_cnt: time counter for animations
        :param critical_distance: if the center of the ghost is less far to the pacman center than the critical
            distance, the pacman is considered to be eaten
        :return: if pacman is eaten
        """
        if self.is_pacman_eaten(critical_distance):
            return True
        if self.field.is_corner(self.center):
            target_point = self._calculate_target(4)
            result_direction = self._follow_target(target_point)
            self.move(result_direction, tick_cnt)
        else:
            self.move(self.previous_movement, tick_cnt)
        return False

    def move_orange(self, tick_cnt: int, critical_distance: int = 10):
        """
        Implements winning strategy of the orange ghost
        :param tick_cnt: time counter for animations
        :param critical_distance: if the center of the ghost is less far to the pacman center than the critical
            distance, the pacman is considered to be eaten
        :return: if pacman is eaten
        """
        if self.is_pacman_eaten(critical_distance):
            return True
        if self.field.is_corner(self.center):
            if calculate_distance(self.center, self.pacman.center) > 8 * 20:
                target_point = self._calculate_target(1)
            else:
                target_point = (123, 580)
            result_direction = self._follow_target(target_point)
            self.move(result_direction, tick_cnt)
        else:
            self.move(self.previous_movement, tick_cnt)
        return False

    def move_randomly(self, tick_cnt: int, critical_distance: int = 10):
        """
        Implements random strategy of the ghost
        :param tick_cnt: time counter for animations
        :param critical_distance: if the center of the ghost is less far to the pacman center than the critical
            distance, the pacman is considered to be eaten
        :return: if pacman is eaten
        """
        if self.is_pacman_eaten(critical_distance):
            return True
        if self.field.is_corner(self.center):
            random_direction = self.change_direction_on_corners()
            self.move(random_direction, tick_cnt)
        else:
            self.move(self.previous_movement, tick_cnt)
        return False

    def is_pacman_eaten(self, critical_distance: int):
        """
        Checks if pacman is eaten
        :param critical_distance: if the center of the ghost is less far to the pacman center than the critical
            distance, the pacman is considered to be eaten
        :return: if pacman is eaten
        """
        distance_to_pacman = calculate_distance(self.center, self.pacman.center)
        if distance_to_pacman < critical_distance:
            return True
        return False
