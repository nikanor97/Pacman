import math
import pygame
from typing import Tuple, Dict, List

from field_config_relations import relation, no_loot_corners, pacman_start_interval
from config import *


class Corner:
    def __init__(self, x: int, y: int):
        self.coord = (x, y)

        self.directions = {
            'up':  None,
            'down': None,
            'left': None,
            'right': None
        }

    def if_possible_to_go(self, direction: str):
        """
        Checks if it is possible to head to the chosen direction
        :param direction: chosen direction
        :return:
        """
        for direct in self.directions:
            if direction == direct and self.directions[direct] is not None:
                return True
        return False


def calculate_distance(coordinate_1: Tuple[int, int], coordinate_2: Tuple[int, int]):
    """
    Calculates distance between tho coordinated
    :param coordinate_1: first coordinate
    :param coordinate_2: second coordinate
    :return: distance
    """
    return math.sqrt((coordinate_1[0] - coordinate_2[0]) ** 2 + (coordinate_1[1] - coordinate_2[1]) ** 2)


class Loot:
    def __init__(self, coord: Tuple[int, int], sprite_name):
        self.coord = coord
        self.is_enabled = True
        self.sprite_name = sprite_name
        self.sprite = pygame.image.load(f"{PATH_IMAGE}\\{sprite_name}.png")


def back_direction(direction: str):
    """
    Get an opposite direction
    :param direction: initial direction
    :return: opposite direction
    """
    res_direction = None
    if direction == 'up':
        res_direction = 'down'
    elif direction == 'down':
        res_direction = 'up'
    elif direction == 'left':
        res_direction = 'right'
    elif direction == 'right':
        res_direction = 'left'
    return res_direction


class Field:
    def __init__(self, loot_pic_name):
        self.corner_relations = relation
        self._loot_pic_name = loot_pic_name

        self.corners: Dict[Tuple[int, int], Corner] = dict()
        self.create_corners()

        self.loot_counter = 0
        self.loot_objects: Dict[Tuple[int, int], Loot] = dict()
        self.create_loot_objects()

    def create_loot_objects(self):
        """
        Creates loot objects on the field
        """
        for coord in self.corners:
            first_corner = self.corners[coord]
            if first_corner.directions['down'] is not None:
                second_corner = self.corners[coord].directions['down']
                if first_corner.coord in no_loot_corners or second_corner.coord in no_loot_corners:
                    pass
                else:
                    y_distance = second_corner.coord[1] - first_corner.coord[1]
                    loot_n_spaces = round(y_distance / LOOT_VERTICAL_SPACE)
                    loot_space = y_distance / loot_n_spaces
                    for i in range(0, loot_n_spaces + 1):
                        x_coord = first_corner.coord[0]
                        y_coord = round(first_corner.coord[1] + i * loot_space)
                        loot_coord = (x_coord, y_coord)
                        if loot_coord not in self.loot_objects:
                            loot = Loot(loot_coord, self._loot_pic_name)
                            self.loot_objects[loot_coord] = loot
                            self.loot_counter += 1
            if first_corner.directions['right'] is not None:
                second_corner = self.corners[coord].directions['right']
                if first_corner.coord in no_loot_corners or second_corner.coord in no_loot_corners \
                        or (first_corner.coord == pacman_start_interval[0]
                            and second_corner.coord == pacman_start_interval[1]):
                    pass
                else:
                    x_distance = second_corner.coord[0] - first_corner.coord[0]
                    loot_n_spaces = round(x_distance / LOOT_HORIZONTAL_SPACE)
                    loot_space = x_distance / loot_n_spaces
                    for i in range(0, loot_n_spaces + 1):
                        x_coord = round(first_corner.coord[0] + i * loot_space)
                        y_coord = first_corner.coord[1]
                        loot_coord = (x_coord, y_coord)
                        if loot_coord not in self.loot_objects:
                            loot = Loot(loot_coord, self._loot_pic_name)
                            self.loot_objects[loot_coord] = loot
                            self.loot_counter += 1

    def create_corners(self):
        """
        Creates corners on the field according to the "field_config_relation.py" file
        """
        for point in self.corner_relations:
            c = Corner(point[0], point[1])
            for idx, key in enumerate(['up', 'down', 'left', 'right']):
                c.directions[key] = self.corner_relations[point][idx]
            self.corners[(point[0], point[1])] = c

        for coord_i in self.corners:
            for key in self.corners[coord_i].directions:
                if self.corners[coord_i].directions[key] is not None:
                    for coord_j in self.corners:
                        if self.corners[coord_i].directions[key] == coord_j:
                            self.corners[coord_i].directions[key] = self.corners[coord_j]
                            break

    def is_corner(self, coords: Tuple[int, int]):
        """
        Checks if the coordinate is a corner
        :param coords:
        :return:
        """
        if coords in self.corners:
            return True
        return False
