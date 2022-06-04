#!/usr/bin/python3

from colorama import Fore, Style, Back
from time import sleep

import numpy as np

from animals import Wolf
from animals import Rabbit
import random

MAX_HEIGHT = 5
MAX_WIDTH = 5

class Area:
    def __init__(self):
        self.grass = Grass() if random.randint(1, 4) == 1 else None
        self.rabbits = [Rabbit()]
        self.wolves = [Wolf()]

class Grass:
    max_size = 20

    def __init__(self, size=10):
        self.size = size

    def grow(self):
        self.size += 1
        if self.size > Grass.max_size:
            self.size = Grass.max_size

def print_world(world):
    print("--------------------------")
    for row in world:
        # Grass
        row_string = "|"
        for cell in row:
            if cell.grass:
                if cell.grass.size >= 10:
                    row_string += f" {Fore.GREEN}{Style.BRIGHT}{str(cell.grass.size)}{Style.RESET_ALL} |"
                else:
                    row_string += f" {Fore.GREEN}{Style.BRIGHT}{str(cell.grass.size)}{Style.RESET_ALL}  |"
            else:
                row_string += "    |"
        print(row_string)

        # Rabbits
        row_string = "|"
        for cell in row:
            if cell.rabbits:
                if len(cell.rabbits) >= 10:
                    row_string += f" {Fore.BLUE}{Style.BRIGHT}{str(len(cell.rabbits))}{Style.RESET_ALL} |"
                else:
                    row_string += f" {Fore.BLUE}{Style.BRIGHT}{str(len(cell.rabbits))}{Style.RESET_ALL}  |"
            else:
                row_string += "    |"
        print(row_string)

        # Wolves
        row_string = "|"
        for cell in row:
            if cell.wolves:
                if len(cell.wolves) >= 10:
                    row_string += f" {Fore.RED}{Style.BRIGHT}{str(len(cell.wolves))}{Style.RESET_ALL} |"
                else:
                    row_string += f" {Fore.RED}{Style.BRIGHT}{str(len(cell.wolves))}{Style.RESET_ALL}  |"
            else:
                row_string += "    |"
        print(row_string)

        print("--------------------------")

def find_neighbours(row_index, cell_index):
    neighbours = []

    possible = [(row_index - 1, cell_index - 1), (row_index - 1, cell_index),
                (row_index - 1, cell_index + 1), (row_index, cell_index - 1),
                (row_index, cell_index + 1), (row_index + 1, cell_index - 1),
                (row_index + 1, cell_index), (row_index + 1, cell_index + 1)]

    for p in possible:
        if 0 <= p[0] <= MAX_WIDTH - 1 and 0 <= p[1] <= MAX_HEIGHT - 1:
            neighbours.append(p)

    return neighbours

def main():
    world = np.array([
                      [Area(), Area(), Area(), Area(), Area()],
                      [Area(), Area(), Area(), Area(), Area()],
                      [Area(), Area(), Area(), Area(), Area()],
                      [Area(), Area(), Area(), Area(), Area()],
                      [Area(), Area(), Area(), Area(), Area()]
                     ])

    print("Original:")
    print_world(world)

    for i in range(1, 11):
        print(f"Iteration {str(i)}:")
        # Grow
        for row_index, row in enumerate(world):
            for cell_index, cell in enumerate(row):
                if cell.grass:
                    cell.grass.grow()

        # Spread seeds
        for row_index, row in enumerate(world):
            for cell_index, cell in enumerate(row):
                if cell.grass:
                    neighbours = find_neighbours(row_index, cell_index)
                    r = random.randint(0, len(neighbours) - 1)
                    s = neighbours[r]
                    if not world[s[0]][s[1]].grass:
                        world[s[0]][s[1]].grass = Grass(1)

        print_world(world)

if __name__ == '__main__':
    main()
