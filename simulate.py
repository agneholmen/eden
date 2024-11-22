from colorama import Fore, Style, Back

import numpy as np

import argparse
import time

from animals import Wolf
from animals import Rabbit
import random

class Area:
    def __init__(self):
        self.grass = Grass() if random.randint(1, 3) == 1 else None
        self.rabbits = [Rabbit()] if random.randint(1, 2) == 1 else []
        self.wolves = [Wolf()] if random.randint(1, 2) == 1 else []

class Grass:
    max_size = 50

    def __init__(self, size=10):
        self.size = size

    def grow(self):
        self.size += 20
        if self.size > Grass.max_size:
            self.size = Grass.max_size

    def eaten(self, amount):
        self.size -= amount
        return amount if self.size >= 0 else amount + self.size

    def exists(self):
        return True if self.size > 0 else False

class World:
    def __init__(self, iterations, max_width, max_height):
        self.iterations = iterations
        self.max_width = max_width
        self.max_height = max_height

        self.map = []
        for _ in range(0, self.max_height):
            row = []
            for _ in range(0, self.max_width):
                row.append(Area())
            self.map.append(row)

    def print_world(self):
        print("--------------------------")
        for row in self.map:
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
            
        print(f"Number of rabbits: {str(self.get_number_of_rabbits())}")
        print(f"Number of grass: {str(self.get_number_of_grass())}")

    def find_neighbours(self, row_index, cell_index):
        neighbours = []

        possible = [(row_index - 1, cell_index - 1), (row_index - 1, cell_index),
                    (row_index - 1, cell_index + 1), (row_index, cell_index - 1),
                    (row_index, cell_index + 1), (row_index + 1, cell_index - 1),
                    (row_index + 1, cell_index), (row_index + 1, cell_index + 1)]

        for p in possible:
            if 0 <= p[0] <= self.max_width - 1 and 0 <= p[1] <= self.max_height - 1:
                neighbours.append(p)

        return neighbours

    def get_random_neighbour(self, row_index, cell_index):
        neighbours = self.find_neighbours(row_index, cell_index)
        r = random.randint(0, len(neighbours) - 1)
        neighbour = neighbours[r]
        
        return neighbour
    
    def get_number_of_rabbits(self):
        rabbits = 0

        for row in self.map:
            for cell in row:
                if cell.rabbits:
                    rabbits += len(cell.rabbits)

        return rabbits
    
    def get_number_of_grass(self):
        grass = 0

        for row in self.map:
            for cell in row:
                if cell.grass:
                    grass += 1

        return grass

def main(iterations, max_height, max_width):
    world = World(iterations, max_height, max_width)

    print("Original:")
    world.print_world()

    for i in range(1, iterations + 1):
        print(f"Iteration {str(i)}:")
        # Grow
        for row_index, row in enumerate(world.map):
            for cell_index, cell in enumerate(row):
                if cell.grass:
                    cell.grass.grow()

        # Spread seeds
        for row_index, row in enumerate(world.map):
            for cell_index, cell in enumerate(row):
                if cell.grass:
                    s = world.get_random_neighbour(row_index, cell_index)
                    if not world.map[s[0]][s[1]].grass:
                        world.map[s[0]][s[1]].grass = Grass(1)

        # Rabbits
        for row_index, row in enumerate(world.map):
            for cell_index, cell in enumerate(row):
                if cell.rabbits:
                    for rabbit in cell.rabbits:
                        # Lose energy
                        rabbit.tire()
                        # Age
                        rabbit.increase_age()
                        # First eat if there's any grass and energy is 40 or below
                        if cell.grass and rabbit.energy <= 40:
                            rabbit.eat_grass(cell.grass)
                            if not cell.grass.exists():
                                cell.grass = None
                        # Otherwise move to different cell or die
                        elif rabbit.energy < 40:
                            if rabbit.is_dead():
                                cell.rabbits.remove(rabbit)
                            else:
                                neighbours = world.find_neighbours(row_index, cell_index)
                                for n in neighbours:
                                    if world.map[n[0]][n[1]].grass:
                                        world.map[n[0]][n[1]].rabbits.append(rabbit)
                                        cell.rabbits.remove(rabbit)
                                        break
                                else:
                                    s = world.get_random_neighbour(row_index, cell_index)
                                    world.map[s[0]][s[1]].rabbits.append(rabbit)
                                    cell.rabbits.remove(rabbit)
                            continue

                        # Attempt to breed. First find partner.
                        if rabbit.breeding == 0 and rabbit.energy > 40:
                            # No other rabbits. Need to move
                            if len(cell.rabbits) == 1:
                                neighbours = world.find_neighbours(row_index, cell_index)
                                for n in neighbours:
                                    if world.map[n[0]][n[1]].rabbits:
                                        world.map[n[0]][n[1]].rabbits.append(rabbit)
                                        cell.rabbits.remove(rabbit)
                                        break
                                else:
                                    s = world.get_random_neighbour(row_index, cell_index)
                                    world.map[s[0]][s[1]].rabbits.append(rabbit)
                                    cell.rabbits.remove(rabbit)
                            else:
                                for partner in cell.rabbits:
                                    if partner != rabbit and partner.sex != rabbit.sex and partner.breeding == 0:
                                        partner.breeding = 5
                                        rabbit.breeding = 5
                                        r = Rabbit()
                                        r.strength = int(((partner.strength + rabbit.strength) / 2) + random.randint(0, 5))
                                        r.agility = int(((partner.agility + rabbit.agility) / 2) + random.randint(0, 5))

                                        cell.rabbits.append(r)
                                        break

                        # Check if dead and remove
                        if rabbit.is_dead():
                            cell.rabbits.remove(rabbit)

        world.print_world()
        time.sleep(3)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--iterations", help="Number of iterations.", type=int, default=10)
    parser.add_argument("-mh", "--height", help="The height of the map in number of cells.", type=int, default=5)
    parser.add_argument("-mw", "--width", help="The width of the map in number of cells.", type=int, default=5)
    args = parser.parse_args()

    main(args.iterations, args.height, args.width)
